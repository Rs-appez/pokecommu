import requests
import json
from pokemonDB import PokemonDB

class PokemonData():

    api_url = 'https://pokeapi.co/api/v2/pokemon/'

    def __init__(self):
        self.db = PokemonDB()

    def get_pokemon_data(self, pokemon_name):

        pokemon = self.db.get_pokemon(pokemon_name)

        if pokemon:
            return pokemon
        else:
            return self.__get_pokemon_from_api(pokemon_name)

    def __get_pokemon_from_api(self, pokemon_name):
        response = requests.get(self.api_url + pokemon_name)
        if response.status_code == 200:
            return self.__save_pokemon(response.json())
        else:
            return None


    def __save_pokemon(self, pokemon_data):
        pokemon = {
            'id': int (pokemon_data['id']),
            'name': pokemon_data['name'],
            'type': pokemon_data['types'],
            'stats': pokemon_data['stats'],
            'height': int (pokemon_data['height']),
            'weight': int (pokemon_data['weight'])
        }
        self.db.save_pokemon(pokemon)
        return pokemon
        