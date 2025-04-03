#!venv/bin/python3
import sys

from pokeBusiness import PokeBusiness

if __name__ == "__main__":
    args = sys.argv
    pb = PokeBusiness()

    # type args
    type = None
    level = None
    speed = None
    hp = None
    defSpe = None
    bst = None

    # sort args
    sort = None
    base = False

    for arg in args[1:]:
        match arg:
            # type args
            case _ if arg.startswith("type="):
                type = arg[5:]
            case _ if arg.startswith("level="):
                level = arg[6:]
            case _ if arg.startswith("speed="):
                speed = arg[6:]
            case _ if arg.startswith("defSpe="):
                defSpe = arg[7:]
            case _ if arg.startswith("hp="):
                hp = arg[3:]
            case _ if arg.startswith("bst="):
                bst = arg[4:]

            # sort args
            case _ if arg.startswith("sort="):
                sort = arg[5:]
            case "base":
                base = True
            case _:
                print(f"Invalid argument: {arg}")
                sys.exit(1)

    pb.auto_trade(
        type=type,
        level=level,
        speed=speed,
        sort=sort,
        hp=hp,
        bst=bst,
        defSpe=defSpe,
        base=base,
    )
