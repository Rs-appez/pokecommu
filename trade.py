#!venv/bin/python3
import sys

from tradeBusiness import TradeBusiness

help_args = [
    ("type=<type>", "Type of the pokemon"),
    ("level=<level>", "Level of the pokemon"),
    ("speed=<speed>", "Speed of the pokemon"),
    ("def=<defense>", "Defense of the pokemon"),
    ("defSpe=<defense>", "Special Defense of the pokemon"),
    ("hp=<hp>", "HP of the pokemon"),
    ("bst=<bst>", "BST of the pokemon"),
    ("sort=<sort>", "Ordering sort : gt/lt (default lt)"),
    ("base", "Base stats only"),
]

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
            case "help" | "-h" | "--help" | "-help":
                print("Usage: python trade.py [args]\nArgs:\n")
                for arg, desc in help_args:
                    print(f"  {arg:<20} {desc}")
                sys.exit(0)
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
                if arg[5:] not in ["lt", "gt"]:
                    print(f"Invalid argument: {arg}")
                    sys.exit(1)
                sort = arg[5:]
            case "base":
                base = True
            case _:
                print(f"Invalid argument: {arg}")
                print("Use 'help' or '-h' for more information")
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
