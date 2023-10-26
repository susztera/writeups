# ----- THIS MIGHT HAVE MISSING ELEMENTS ------ #

# A day before the memorial of the Dying Sun, Miyuki began talking about Broider, a death squad commander and a friend of Paulie’s capturer. He would be a party guest at 
# Viryr’s palace. After examining a lot of different scenarios, Miyuki came up with a plan in which Paulie would lure Broider to a secluded location so the group could capture
# him. Following the plan, a wild chase had just begun when the two looked each other in the eye. After an extremely risky manoeuvre, Paulie outwitted Broider and led him into
# an alley in Vinyr’s undercity. The plan was a success. Your squad had managed to capture Broider and bring him back to the ship. After hours of interrogation by Ulysses, he
# revealed the final key to a series of encrypted messages. Can you find a way to decrypt the others? The flag consists entirely of uppercase characters and has the form 
# HTB{SOMETHINGHERE}. You still have to add the {} yourself.

import os

with open('super_secret_messages.txt', 'r') as f:
    SUPER_SECRET_MESSAGES = [msg.strip() for msg in f.readlines()]

def deriveKey(key):
    derived_key = []

    for i, char in enumerate(key):
        previous_letters = key[:i]
        new_number = 1
        for j, previous_char in enumerate(previous_letters):
            if previous_char > char:
                derived_key[j] += 1
            else:
                new_number += 1
        derived_key.append(new_number)
    return derived_key

def transpose(array):
    return [row for row in map(list, zip(*array))]

def flatten(array):
    return "".join([i for sub in array for i in sub])

def twistedColumnarEncrypt(pt, key):
    derived_key = deriveKey(key)

    width = len(key)

    blocks = [pt[i:i + width] for i in range(0, len(pt), width)]
    blocks = transpose(blocks)

    ct = [blocks[derived_key.index(i + 1)][::-1] for i in range(width)]
    ct = flatten(ct)
    return ct

class PRNG:
    def __init__(self, seed):
        self.p = 0x2ea250216d705
        self.a = self.p
        self.b = int.from_bytes(os.urandom(16), 'big')
        self.rn = seed

    def next(self):
        self.rn = ((self.a * self.rn) + self.b) % self.p
        return self.rn

def main():
    seed = int.from_bytes(os.urandom(16), 'big')
    rng = PRNG(seed)

    cts = ""

    for message in SUPER_SECRET_MESSAGES:
        key = str(rng.next())
        ct = twistedColumnarEncrypt(message, key)
        cts += ct + "\n"

    with open('encrypted_messages.txt', 'w') as f:
        f.write(cts)

    dialog = "Miyuki says:\n"
    dialog += "Klaus it's your time to sign!\n"
    dialog += "All we have is the last key of this wierd encryption scheme.\n"
    dialog += "Please do your magic, we need to gather more information if we want to defeat Draeger.\n"
    dialog += f"The key is: {str(key)}\n"

    with open('dialog.txt', 'w') as f:
        f.write(dialog)

if __name__ == '__main__':
    main()
