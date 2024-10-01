from decouple import config
import requests

class PokeCommu():

    url = 'https://poketwitch.bframework.de/api/game/ext/trainer/'

    url_poke = url + 'pokemon/'
    url_inventory = url + 'inventory/v2/'
    url_trade = url + "wonder-trade/"

    token = config('PCG_TOKEN')

    def __init__(self):
        self.pokemons = []
        self.inventory = []

        self.refresh_all()

    def refresh_all(self):
        if not (self.get_pokemon() and self.get_inventory()):
            print("Error while refreshing")
            return False
        return True


    def get_pokemon(self):
        response = requests.get(self.url_poke, headers={'Authorization': self.token})
        if response.status_code == 200:
            for pokemon in response.json()["allPokemon"]:
                if not pokemon['isShiny']:
                    self.pokemons.append(pokemon)
            return True
        else:
            return False
        
    def get_inventory(self):
        response = requests.get(self.url_inventory, headers={'Authorization': self.token})
        if response.status_code == 200:
            for ball in response.json()["allItems"]:
                if ball["type"] == 2 :
                    self.inventory.append(ball)
            return True
        else:
            return False
        
    def trade_pokemon(self, pokemon_id):

        response = requests.post(self.url_trade + str(pokemon_id) + "/", headers={'Authorization': self.token})
        print(response.content)
        if response.status_code == 200:
            return True
        else:
            return False
        
    def auto_trade(self):
        pokemon = self.__find_pokemon_to_trade()
        self.trade_pokemon(pokemon['id'])

    def __get_first_duplicated_pokemon(self):
        seen = set()
        for pokemon in self.pokemons:
            name = pokemon.get('pokedexId')
            if name in seen:
                return pokemon
            seen.add(name)
        return None
    
    def __find_pokemon_to_trade(self):
        duplicated_pokemon = self.__get_first_duplicated_pokemon()

        if duplicated_pokemon:
            pokemons_to_trade = self.__get_all_pokemons_by_id(duplicated_pokemon['pokedexId'])
            pokemons_to_trade.sort(key=lambda x: x['lvl'])

            print(f"Trading {pokemons_to_trade[0]['name']} lvl {pokemons_to_trade[0]['lvl']} id {pokemons_to_trade[0]['id']}")

            return pokemons_to_trade[0]

    def __get_all_pokemons_by_id(self, id):
        return [pokemon for pokemon in self.pokemons if pokemon.get('pokedexId') == id]