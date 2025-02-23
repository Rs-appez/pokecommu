import sys

from pokeBusiness import PokeBusiness

if __name__ == "__main__":
    type = None
    level = None
    speed = None
    hp = None
    defSpe = None

    sort = None
    base = False

    args = sys.argv

    for arg in args:
        if arg.startswith("type="):
            type = arg[5:]
        if arg.startswith("level="):
            level = arg[6:]
        if arg.startswith("speed="):
            speed = arg[6:]
        if arg.startswith("defSpe="):
            defSpe = arg[7:]
        if arg.startswith("hp="):
            hp = arg[3:]

        if arg.startswith("sort="):
            sort = arg[5:]
        if arg.startswith("base"):
            base = True

    pb = PokeBusiness()
    pb.auto_trade(
        type=type, level=level, speed=speed, sort=sort, hp=hp, defSpe=defSpe, base=base
    )
