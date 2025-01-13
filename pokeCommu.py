from decouple import config
import requests


class PokeCommu:

    url = "https://poketwitch.bframework.de/api/game/ext/"

    url_trainer = url + "trainer/"
    url_shop = url + "shop/"

    url_poke = url_trainer + "pokemon/"
    url_inventory = url_trainer + "inventory/v2/"
    url_trade = url_trainer + "wonder-trade/"

    url_purchase = url_shop + "purchase/"

    token = config("PCG_TOKEN")
    header = {"Authorization": token}

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
        response = requests.get(self.url_poke, headers=self.header)
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
        response = requests.get(self.url_inventory, headers=self.header)
        if response.status_code == 200:
            for ball in response.json()["allItems"]:
                if ball["type"] == 2:
                    self.inventory.append(ball)
            return True
        else:
            return False

    def trade_pokemon(self, pokemon_id):

        response = requests.post(
            self.url_trade + str(pokemon_id) + "/", headers=self.header
        )
        print(response.content)
        if response.status_code == 200:
            return True
        else:
            return False

    def buy_item(self, item, amount=1):

        data = {"amount": amount, "item_name": item}

        response = requests.post(self.url_purchase, headers=self.header, data=data)

        print(response.json())
        if response.status_code == 200:
            return True
        return False
