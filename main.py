#!venv/bin/python3
import sys
from twitchBot import TwitchBot
from pokeBusiness import PokeBusiness

help_args = [
    ("all=<true|false>", "Catch all pokemon (default true)"),
    ("type=<type>", "Type of the pokemon"),
    ("weight=<weight>", "Weight of the pokemon"),
    ("ball=<ball_type>", "Type of the ball to use"),
    ("partial", "Catch partial pokemon (default false)"),
    ("special", "Catch special pokemon (default false)"),
    ("gt,lt", "Use greater/less than for weight comparison (default greater than)"),
]

if __name__ == "__main__":
    args = sys.argv
    cath_all = True
    partial = False
    special = False
    greater = True

    poke_type = None
    poke_weight = None
    ball_type = None

    for arg in args[1:]:
        match arg:
            case "help" | "-h" | "--help" | "-help":
                print("Usage: python main.py [args]\nArgs:\n")
                for arg, desc in help_args:
                    print(f"  {arg:<20} {desc}")
                sys.exit(0)
            case _ if arg.startswith("all="):
                if arg[4:].lower() in ["true", "false"]:
                    cath_all = arg[4:].lower() == "true"
                else:
                    print(f"Invalid argument: {arg}")
                    sys.exit(1)
            case _ if arg.startswith("type="):
                poke_type = arg[5:]
                cath_all = False
            case _ if arg.startswith("weight="):
                try:
                    poke_weight = float(arg[7:])
                    cath_all = False
                except ValueError:
                    print(f"Invalid weight value: {arg[7:]}")
                    sys.exit(1)
            case _ if arg.startswith("ball="):
                ball_type = arg[5:]
            case "partial":
                cath_all = False
                partial = True
            case "special":
                cath_all = False
                special = True
            case "lt":
                greater = False
            case "gt":
                greater = True
            case _:
                print(f"Invalid argument: {arg}")
                sys.exit(1)

    pkb = PokeBusiness(
        catch_all=cath_all,
        poke_type=poke_type,
        poke_weight=poke_weight,
        ball_type=ball_type,
        partial=partial,
        special=special,
        greater=greater,
    )

    bot = TwitchBot(pkb)
