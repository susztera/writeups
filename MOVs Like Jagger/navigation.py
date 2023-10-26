from ecdsa import ellipticcurve as ecc
from random import randint

a = -35
b = 98
p = 434252269029337012720086440207
Gx = 16378704336066569231287640165
Gy = 377857010369614774097663166640
ec_order = 434252269029337012720086440208

E = ecc.CurveFp(p, a, b)
G = ecc.Point(E, Gx, Gy, ec_order)

def generateKeyPair():
    private = randint(1, 2**64)
    public = G * private
    return(public, private)


def checkDestinationPoint(data: dict, P: ecc.Point, nQ: int, E: ecc.CurveFp) -> list:
    destination_x, destination_y = checkCoordinates(data)
    destination_point = ecc.Point(E, destination_x, destination_y, ec_order)
    secret_point = P * nQ
    same_x = destination_point.x() == secret_point.x()
    same_y = destination_point.y() == secret_point.y()

    if (same_x and same_y):
        return True
    else:
        return False
