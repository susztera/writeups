# Description
Amidst the dystopian chaos, the LoanPool stands as a beacon for the oppressed, allowing the brave to deposit tokens in support of the cause. Your mission, should you choose to accept it, is to exploit the system's vulnerabilities and siphon tokens from this pool, a daring act of digital subterfuge aimed at weakening the regime's economic stronghold. Success means redistributing wealth back to the people, a crucial step towards undermining the oppressors' grip on power.
# Errors.sol
```py
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

error NotSupported(address token);
error CallbackFailed();
error LoanNotRepaid();
error InsufficientBalance();
```
# Events.sol
```py
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

interface Events {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event FlashLoanSuccessful(
        address indexed target, address indexed initiator, address indexed token, uint256 amount, uint256 fee
    );
    event FeesUpdated(address indexed token, address indexed user, uint256 fees);
}
```
# FixedPointMath.sol
```py
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

library FixedMathLib {
    function fixedMulFloor(uint256 self, uint256 b, uint256 denominator) internal pure returns (uint256) {
        return self * b / denominator;
    }

    function fixedMulCeil(uint256 self, uint256 b, uint256 denominator) internal pure returns (uint256 result) {
        uint256 _mul = self * b;
        if (_mul % denominator == 0) {
            result = _mul / denominator;
        } else {
            result = _mul / denominator + 1;
        }
    }

    function fixedDivFloor(uint256 self, uint256 b, uint256 denominator) internal pure returns (uint256) {
        return self * denominator / b;
    }

    function fixedDivCeil(uint256 self, uint256 b, uint256 denominator) internal pure returns (uint256 result) {
        uint256 _mul = self * denominator;
        if (_mul % b == 0) {
            result = _mul / b;
        } else {
            result = _mul / b + 1;
        }
    }
}
```
# Interfaces.sol
```py
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

interface IERC20Minimal {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

interface IERC3156FlashBorrower {
    function onFlashLoan(address initiator, address token, uint256 amount, uint256 fee, bytes calldata data)
        external
        returns (bytes32);
}
```
# LoanPool.sol
```py
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {FixedMathLib} from "./FixedPointMath.sol";
import "./Errors.sol";
import {IERC20Minimal, IERC3156FlashBorrower} from "./Interfaces.sol";
import {Events} from "./Events.sol";

struct UserRecord {
    uint256 feePerShare;
    uint256 fees;
    uint256 balance;
}

contract LoanPool is Events {
    using FixedMathLib for uint256;

    uint256 constant BONE = 10 ** 18;

    address public underlying;
    uint256 public totalSupply;
    uint256 public feePerShare;
    mapping(address => UserRecord) public userRecords;

    constructor(address _underlying) {
        underlying = _underlying;
    }

    function deposit(uint256 amount) external {
        address _msgsender = msg.sender;

        _updateFees(_msgsender);
        IERC20Minimal(underlying).transferFrom(_msgsender, address(this), amount);

        _mint(_msgsender, amount);
    }

    function withdraw(uint256 amount) external {
        address _msgsender = msg.sender;

        if (userRecords[_msgsender].balance < amount) {
            revert InsufficientBalance();
        }

        _updateFees(_msgsender);
        _burn(_msgsender, amount);

        // Send also any fees accumulated to user
        uint256 fees = userRecords[_msgsender].fees;
        if (fees > 0) {
            userRecords[_msgsender].fees = 0;
            amount += fees;
            emit FeesUpdated(underlying, _msgsender, fees);
        }

        IERC20Minimal(underlying).transfer(_msgsender, amount);
    }

    function balanceOf(address account) public view returns (uint256) {
        return userRecords[account].balance;
    }

    // Flash loan EIP
    function maxFlashLoan(address token) external view returns (uint256) {
        if (token != underlying) {
            revert NotSupported(token);
        }
        return IERC20Minimal(token).balanceOf(address(this));
    }

    function flashFee(address token, uint256 amount) external view returns (uint256) {
        if (token != underlying) {
            revert NotSupported(token);
        }
        return _computeFee(amount);
    }

    function flashLoan(IERC3156FlashBorrower receiver, address token, uint256 amount, bytes calldata data)
        external
        returns (bool)
    {
        if (token != underlying) {
            revert NotSupported(token);
        }

        IERC20Minimal _token = IERC20Minimal(underlying);
        uint256 _balanceBefore = _token.balanceOf(address(this));

        if (amount > _balanceBefore) {
            revert InsufficientBalance();
        }

        uint256 _fee = _computeFee(amount);
        _token.transfer(address(receiver), amount);

        if (
            receiver.onFlashLoan(msg.sender, underlying, amount, _fee, data)
                != keccak256("ERC3156FlashBorrower.onFlashLoan")
        ) {
            revert CallbackFailed();
        }

        uint256 _balanceAfter = _token.balanceOf(address(this));
        if (_balanceAfter < _balanceBefore + _fee) {
            revert LoanNotRepaid();
        }

        // Accumulate fees and update feePerShare
        uint256 interest = _balanceAfter - _balanceBefore;
        feePerShare += interest.fixedDivFloor(totalSupply, BONE);

        emit FlashLoanSuccessful(address(receiver), msg.sender, token, amount, _fee);
        return true;
    }

    // Private methods
    function _mint(address to, uint256 amount) private {
        totalSupply += amount;
        userRecords[to].balance += amount;

        emit Transfer(address(0), to, amount);
    }

    function _burn(address from, uint256 amount) private {
        totalSupply -= amount;
        userRecords[from].balance -= amount;

        emit Transfer(from, address(0), amount);
    }

    function _updateFees(address _user) private {
        UserRecord storage record = userRecords[_user];
        uint256 fees = record.balance.fixedMulCeil((feePerShare - record.feePerShare), BONE);

        record.fees += fees;
        record.feePerShare = feePerShare;

        emit FeesUpdated(underlying, _user, fees);
    }

    function _computeFee(uint256 amount) private pure returns (uint256) {
        // 0.05% fee
        return amount.fixedMulCeil(5 * BONE / 10_000, BONE);
    }
}
```
# Setup.sol
```py
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {LoanPool} from "./LoanPool.sol";
import {Token} from "./Token.sol";

contract Setup {
    LoanPool public immutable TARGET;
    Token public immutable TOKEN;

    constructor(address _user) {
        TOKEN = new Token(_user);
        TARGET = new LoanPool(address(TOKEN));

        TOKEN.approve(address(TARGET), type(uint256).max);
        TARGET.deposit(10 ether);
    }

    function isSolved() public view returns (bool) {
        return (TARGET.totalSupply() == 10 ether && TOKEN.balanceOf(address(TARGET)) < 10 ether);
    }
}
```
# Token.sol
```py
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Events} from "./Events.sol";

contract Token is Events {
    string public name = "Token";
    string public symbol = "Tok";
    uint8 public immutable decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    constructor(address _user) payable {
        _mint(msg.sender, 10 ether);
        _mint(_user, 1 ether);
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        allowance[msg.sender][spender] = amount;

        emit Approval(msg.sender, spender, amount);

        return true;
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;

        emit Transfer(msg.sender, to, amount);

        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        allowance[from][msg.sender] -= amount;

        balanceOf[from] -= amount;
        balanceOf[to] += amount;

        emit Transfer(from, to, amount);

        return true;
    }

    function _mint(address to, uint256 amount) private {
        balanceOf[to] += amount;
        totalSupply += amount;

        emit Transfer(address(0), to, amount);
    }

    function _burn(address from, uint256 amount) private {
        balanceOf[from] -= amount;
        totalSupply -= amount;

        emit Transfer(from, address(0), amount);
    }
}
```
