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
    ("weight=<weight>", "Weight of the pokemon"),
    ("bst=<bst>", "BST of the pokemon"),
    ("sort=<sort>", "Ordering sort : gt/lt (default lt)"),
    ("base", "Base stats only"),
    ("help", "Show this help message"),
]

if __name__ == "__main__":
    args = sys.argv

    # type args
    poke_type = None
    level = None
    speed = None
    hp = None
    weight = None
    defSpe = None
    defense = None
    bst = None

    # sort args
    greater = True
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
                try:
                    level = int(arg[6:])
                except ValueError:
                    print(f"Invalid level value: {arg[6:]}")
                    sys.exit(1)
            case _ if arg.startswith("speed="):
                try:
                    speed = int(arg[6:])
                except ValueError:
                    print(f"Invalid speed value: {arg[6:]}")
                    sys.exit(1)
            case _ if arg.startswith("weight="):
                try:
                    weight = float(arg[7:])
                except ValueError:
                    print(f"Invalid weight value: {arg[7:]}")
                    sys.exit(1)
            case _ if arg.startswith("def="):
                try:
                    defense = int(arg[4:])
                except ValueError:
                    print(f"Invalid defense value: {arg[4:]}")
                    sys.exit(1)
            case _ if arg.startswith("defSpe="):
                try:
                    defSpe = int(arg[7:])
                except ValueError:
                    print(f"Invalid special defense value: {arg[7:]}")
                    sys.exit(1)
            case _ if arg.startswith("hp="):
                try:
                    hp = int(arg[3:])
                except ValueError:
                    print(f"Invalid HP value: {arg[3:]}")
                    sys.exit(1)
            case _ if arg.startswith("bst="):
                try:
                    bst = int(arg[4:])
                except ValueError:
                    print(f"Invalid BST value: {arg[4:]}")
                    sys.exit(1)

            # sort args
            case _ if arg.startswith("sort="):
                if arg[5:] not in ["lt", "gt"]:
                    print(f"Invalid argument: {arg}")
                    sys.exit(1)
                greater = arg[5:] == "gt"
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
        weight=weight,
        greater=greater,
        hp=hp,
        bst=bst,
        defense=defense,
        defSpe=defSpe,
        base=base,
    )
    tb.auto_trade()
