#!venv/bin/python3
import sys
from twitchBot import TwitchBot
from pokeBusiness import PokeBusiness

help_args = [
    ("all=<true|false>", "Catch all pokemon (default true)"),
    (
        "hardpokedex=<true|false>",
        "Catch only pokemon not in special pokedex (default false)",
    ),
    ("type=<type>", "Type of the pokemon"),
    ("weight=<weight>", "Weight of the pokemon"),
    ("ball=<ball_type>", "Type of the ball to use"),
    ("gen=<generation>", "Generation of the pokemon"),
    ("partial", "Catch partial pokemon (default false)"),
    ("special", "Catch special pokemon (default false)"),
    ("gt,lt", "Use greater/less than for weight comparison (default greater than)"),
    ("help", "Show this help message"),
]


def display_help():
    print("Usage: python main.py [args]\nArgs:\n")
    for arg, desc in help_args:
        print(f"  {arg:<20} {desc}")


if __name__ == "__main__":
    args = sys.argv
    cath_all = True
    hard_pokedex = False
    partial = False
    special = False
    greater = True

    poke_type = None
    poke_weight = None
    poke_generation = None
    ball_type = None

    for arg in args[1:]:
        match arg:
            case "help" | "-h" | "--help" | "-help":
                display_help()
                sys.exit(0)
            case _ if arg.startswith("all="):
                if arg[4:].lower() in ["true", "false"]:
                    cath_all = arg[4:].lower() == "true"
                else:
                    print(f"Invalid argument: {arg}")
                    sys.exit(1)
            case _ if arg.startswith("hardpokedex="):
                if arg[12:].lower() in ["true", "false"]:
                    hard_pokedex = arg[12:].lower() == "true"
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
            case _ if arg.startswith("gen="):
                try:
                    poke_generation = int(arg[4:])
                    cath_all = False
                except ValueError:
                    print(f"Invalid generation value: {arg[4:]}")
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
                display_help()
                sys.exit(1)

    pkb = PokeBusiness(
        catch_all=cath_all,
        hard_pokedex=hard_pokedex,
        poke_type=poke_type,
        poke_weight=poke_weight,
        poke_generation=poke_generation,
        ball_type=ball_type,
        partial=partial,
        special=special,
        greater=greater,
    )

    bot = TwitchBot(pkb)
