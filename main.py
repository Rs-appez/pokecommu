from twitchBot import TwitchBot
from pokeBusiness import PokeBusiness

if __name__ == '__main__':
    
    pkb = PokeBusiness()

    # print(pkb.catch_pokemon("Nidoran♂"))

    bot = TwitchBot(pkb)


    
    # pc = PokeCommu()
    # pc.auto_trade()
