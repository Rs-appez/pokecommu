#!venv/bin/python3
import sys
from twitchBot import TwitchBot
from pokeBusiness import PokeBusiness

if __name__ == "__main__":
    args = sys.argv
    cath_all = True
    partial = False

    poke_type = None
    ball_type = None

    for arg in args[1:]:
        match arg:
            case _ if arg.startswith("all="):
                if arg[4:].lower() in ["true", "false"]:
                    cath_all = arg[4:].lower() == "true"
                else:
                    print(f"Invalid argument: {arg}")
                    sys.exit(1)
            case _ if arg.startswith("type="):
                poke_type = arg[5:]
                cath_all = False
            case _ if arg.startswith("ball="):
                ball_type = arg[5:]
            case "partial":
                cath_all = False
                partial = True
            case _:
                print(f"Invalid argument: {arg}")
                sys.exit(1)

    pkb = PokeBusiness(
        catch_all=cath_all, poke_type=poke_type, ball_type=ball_type, partial=partial
    )

    bot = TwitchBot(pkb)
