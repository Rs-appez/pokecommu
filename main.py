import sys
from twitchBot import TwitchBot
from pokeBusiness import PokeBusiness

if __name__ == "__main__":
    args = sys.argv
    cath_all = True

    for arg in args[1:]:
        match arg:
            case _ if arg.startswith("all="):
                try:
                    cath_all = bool(arg[4:])
                except ValueError:
                    print(f"Invalid argument: {arg}")
                    sys.exit(1)
            case _:
                print(f"Invalid argument: {arg}")
                sys.exit(1)

    pkb = PokeBusiness(catch_all=cath_all)

    bot = TwitchBot(pkb)
