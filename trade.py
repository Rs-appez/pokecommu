#!venv/bin/python3
import sys

from tradeBusiness import TradeBusiness

if __name__ == "__main__":
    args = sys.argv

    # type args
    poke_type = None
    level = None
    speed = None
    hp = None
    defSpe = None
    defense = None
    bst = None

    # sort args
    sort = None
    base = False

    for arg in args[1:]:
        match arg:
            # type args
            case _ if arg.startswith("type="):
                poke_type = arg[5:]
            case _ if arg.startswith("level="):
                level = arg[6:]
            case _ if arg.startswith("speed="):
                speed = arg[6:]
            case _ if arg.startswith("def="):
                defense = arg[4:]
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

    tb = TradeBusiness(
        poke_type=poke_type,
        level=level,
        speed=speed,
        sort=sort,
        hp=hp,
        bst=bst,
        defense=defense,
        defSpe=defSpe,
        base=base,
    )
    tb.auto_trade()
