import sys

from pokeBusiness import PokeBusiness

if __name__ == "__main__":

    type = None

    args = sys.argv

    for arg in args:
        if arg.startswith("type="):
            type = arg[5:]
    pb = PokeBusiness()
    pb.auto_trade(type=type)
