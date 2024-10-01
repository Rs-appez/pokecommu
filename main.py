from pokemonData import PokemonData
from pokeCommu import PokeCommu
from twitchBot import TwitchBot
from pokeBusiness import PokeBusiness

if __name__ == '__main__':
    
    # pkb = PokeBusiness()

    # bot = TwitchBot(pkb)

    pkd = PokemonData()

    print(pkd.get_pokemon_data("Insecateur"))
    
    # pc = PokeCommu()
    # pc.auto_trade()
