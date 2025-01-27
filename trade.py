import sys

from pokeBusiness import PokeBusiness

if __name__ == "__main__":

    type = None
    level = None

    args = sys.argv

    for arg in args:
        if arg.startswith("type="):
            type = arg[5:]
        if arg.startswith("level="):
            level = arg[6:]

    pb = PokeBusiness()
    pb.auto_trade(type=type, level=level)
