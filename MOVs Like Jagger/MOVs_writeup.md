# MOVs Like Jagger

The challenge comes down to a mathematical principle, elliptic curves and their multiplication.

The secret location is P elliptic curve point multiplied by nQ number. We get P elliptic curve point if we produce a value error on the site (present_x and present_y). We also get Q elliptic curve point which was produced by multiplying G elliptic curve point by nQ.

We get told the values of G and Q. This means the location calculation is vulnerable to MOV attack (given A and r*A, find r). 

Used [this](https://github.com/jvdsn/crypto-attacks/blob/master/attacks/ecc/mov_attack.py) tool. Modified to match the right data for Q:


```python
import logging
from math import gcd
from sage.all import GF
from sage.all import discrete_log

a = -35
b = 98
p = 434252269029337012720086440207
Gx = 16378704336066569231287640165
Gy = 377857010369614774097663166640

E = EllipticCurve(GF(p), [a,b])
G = E([Gx,Gy])
F = E([157791589626377674787292446653,274130657323674068142841227900])

def attack(P, R, max_k=6, max_tries=10):
    """
    Solves the discrete logarithm problem using the MOV attack.
    More information: Harasawa R. et al., "Comparing the MOV and FR Reductions in Elliptic Curve Cryptography" (Section 2)
    :param P: the base point
    :param R: the point multiplication result
    :param max_k: the maximum value of embedding degree to try (default: 6)
    :param max_tries: the maximum amount of times to try to find l (default: 10)
    :return: l such that l * P == R, or None if l was not found
    """
    E = P.curve()
    q = E.base_ring().order()
    n = P.order()
    assert gcd(n, q) == 1, "GCD of generator order and curve base ring order should be 1."

    logging.info("Calculating embedding degree...")
    for k in range(1, max_k + 1):
        if q ** k % n == 1:
            break
    else:
        return None

    logging.info(f"Found embedding degree {k}")
    Ek = E.base_extend(GF(q ** k))
    Pk = Ek(P)
    Rk = Ek(R)
    for i in range(max_tries):
        Q_ = Ek.random_point()
        m = Q_.order()
        d = gcd(m, n)
        Q = (m // d) * Q_
        if Q.order() != n:
            continue

        if (alpha := Pk.weil_pairing(Q, n)) == 1:
            continue

        beta = Rk.weil_pairing(Q, n)
        logging.info(f"Computing discrete_log({beta}, {alpha})...")
        l = discrete_log(beta, alpha)
        return int(l)

    return None
attack(G,F)
```
nQ is **10131318009579915944**
.

From there, the calculation
```python
from ecdsa import ellipticcurve as ecc

a = -35
b = 98
p = 434252269029337012720086440207
Gx = 16378704336066569231287640165
Gy = 377857010369614774097663166640
ec_order = 434252269029337012720086440208

E = ecc.CurveFp(p, a, b)
G = ecc.Point(E, Gx, Gy, ec_order)
F = ecc.Point(E,72889381271618295933851461177,315657093527921193551001937272,ec_order)
loc = F*10131318009579915944
print(hex(loc.x()))
print(hex(loc.y()))
```
worked perfectly for secret_location x and y:
```
❯ python3 mov_attack.py
0x2e7dca158c2f1f749ef93e89e
0xf23cefe452ae74796513ec71
```
HTB{I7_5h0075_,1t_m0v5,_wh47_15_i7?}
