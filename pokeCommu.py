from decouple import config
import requests


class PokeCommu:

    url = "https://poketwitch.bframework.de/api/game/ext/trainer/"

    url_poke = url + "pokemon/"
    url_inventory = url + "inventory/v2/"
    url_trade = url + "wonder-trade/"

    token = config("PCG_TOKEN")

    def __init__(self):
        self.pokemons = []
        self.pokemons_shiny = []
        self.inventory = []

        self.refresh_all()

    def refresh_all(self):
        if not (self.get_pokemon() and self.get_inventory()):
            print("Error while refreshing")
            return False
        return True

    def get_pokemon(self):
        response = requests.get(self.url_poke, headers={"Authorization": self.token})
        if response.status_code == 200:
            for pokemon in response.json()["allPokemon"]:
                if not pokemon["isShiny"]:
                    self.pokemons.append(pokemon)
                else:
                    self.pokemons_shiny.append(pokemon)
            return True
        else:
            return False

    def get_inventory(self):
        response = requests.get(
            self.url_inventory, headers={"Authorization": self.token}
        )
        if response.status_code == 200:
            for ball in response.json()["allItems"]:
                if ball["type"] == 2:
                    self.inventory.append(ball)
            return True
        else:
            return False

    def trade_pokemon(self, pokemon_id):

        response = requests.post(
            self.url_trade + str(pokemon_id) + "/",
            headers={"Authorization": self.token},
        )
        print(response.content)
        if response.status_code == 200:
            return True
        else:
            return False
