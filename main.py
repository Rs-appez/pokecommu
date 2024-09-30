from pokemonData import PokemonData


if __name__ == '__main__':
    pkd = PokemonData()
    pokemon = pkd.get_pokemon_data('zorua')
    print(pokemon)