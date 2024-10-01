import requests
from pokemonDB import PokemonDB
import json

from unidecode import unidecode
class PokemonData():

    api_url = 'https://tyradex.vercel.app/api/v1/pokemon/'

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

        name_fr = unidecode(pokemon_data['name']['fr'])

        height = float (pokemon_data['height'].replace(' m', '').replace(',', '.'))
        weight = float (pokemon_data['weight'].replace(' kg', '').replace(',', '.'))

        pokemon = {
            'id': int (pokemon_data['pokedex_id']),
            'name_fr': name_fr,
            'name_en': pokemon_data['name']['en'],
            'type': pokemon_data['types'],
            'stats': pokemon_data['stats'],
            'height': height,
            'weight': weight
        }
        self.db.save_pokemon(pokemon)
        return pokemon
        