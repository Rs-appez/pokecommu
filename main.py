from pokemonData import PokemonData
from pokeCommu import PokeCommu


if __name__ == '__main__':
    pokeData = PokemonData()
    pokeCommu = PokeCommu()

    duplicated_pokemon = pokeCommu.find_pokemon_to_trade()
