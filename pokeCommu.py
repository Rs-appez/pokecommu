from itertools import chain
from decouple import config
import requests

from pokemon import Pokemon


class PokeCommu:
    url = "https://poketwitch.bframework.de/api/game/ext/"

    url_trainer = url + "trainer/"
    url_shop = url + "shop/"

    url_poke = url_trainer + "pokemon/v2/"
    url_poke_v3 = url_trainer + "pokemon/v3/"
    url_inventory = url_trainer + "inventory/v3/"
    url_trade = url_trainer + "wonder-trade/"

    url_purchase = url_shop + "purchase/"

    token = config("PCG_TOKEN")
    header = {"Authorization": token}

    def __init__(self):
        self.pokemons = []
        self.pokemons_locked = []
        self.pokemons_shiny = []
        self.eggs = []
        self.inventory = []

        self.cash = 0

        self.refresh_all()

    def refresh_all(self):
        if not (self.load_pokemon() and self.load_inventory()):
            print("Error while refreshing")
            return False
        else:
            self.__auto_buy_ultraball()

        return True

    def load_pokemon(self):
        response = requests.get(self.url_poke, headers=self.header)
        if response.status_code == 200:
            for pokemon in response.json()["allPokemon"]:
                pokemon["name"] = pokemon["name"].lower()
                if "egg" in pokemon["name"].split("-"):
                    self.eggs.append(pokemon)
                elif pokemon["locked"]:
                    self.pokemons_locked.append(pokemon)
                elif pokemon["isShiny"]:
                    self.pokemons_shiny.append(pokemon)
                else:
                    self.pokemons.append(pokemon)
            return True
        else:
            return False

    def load_inventory(self):
        response = requests.get(self.url_inventory, headers=self.header)
        if response.status_code == 200:
            json_response = response.json()
            self.cash = json_response["cash"]
            for ball in json_response["allItems"]:
                if ball["type"] == 2:
                    self.inventory.append(ball)
            return True
        else:
            return False

    def get_pokemon(self, pokemon_id) -> dict | None:
        response = requests.get(
            self.url_poke_v3 + str(pokemon_id) + "/", headers=self.header
        )
        if response.status_code == 200:
            poke_data = response.json()
            return poke_data
        else:
            return None

    def trade_pokemon(self, pokemon_id):
        response = requests.post(
            self.url_trade + str(pokemon_id) + "/", headers=self.header
        )
        if response.status_code == 200:
            poke_id = response.json()["pokemon"]["order"]
            poke_name = response.json()["pokemon"]["name"]
            poke_level = response.json()["pokemon"]["lvl"]
            poke_avgIV = response.json()["pokemon"]["avgIV"]

            poke_data = {
                "id": poke_id,
                "name": poke_name,
                "lvl": poke_level,
                "avgIV": poke_avgIV,
            }
            return poke_data
        else:
            return 0

    def buy_item(self, item, amount=1, refresh=True):
        data = {"amount": amount, "item_name": item}

        response = requests.post(
            self.url_purchase, headers=self.header, data=data)

        if response.status_code == 200:
            print(f"Bought {amount} {item}")
            if refresh:
                self.load_inventory()
            return True
        return False

    def is_pokemon_in_inventory(self, pokemon: Pokemon) -> bool:
        poke_name = pokemon.get_pcg_name()

        if any(
            poke["name"] == poke_name
            for poke in chain(self.pokemons, self.pokemons_shiny, self.pokemons_locked)
        ):
            return True
        return False

    def is_shiny_in_inventory(self, pokemon: Pokemon) -> bool:
        poke_name = pokemon.get_pcg_name()

        if any(poke["name"] == poke_name for poke in self.pokemons_shiny):
            return True
        return False

    def check_ball_in_inventary(self, ball) -> bool:
        if [b for b in self.inventory if b["name"] == ball]:
            ball = [b for b in self.inventory if b["name"] == ball][0]
            if ball["amount"] > 0:
                return True

        return False

    def remove_ball_from_inventory(self, ball) -> bool:
        if [b for b in self.inventory if b["name"] == ball]:
            ball = [b for b in self.inventory if b["name"] == ball][0]
            if ball["amount"] > 0:
                ball["amount"] -= 1
                return True

        return False

    def __auto_buy_ultraball(self):
        if [b for b in self.inventory if b["name"] == "ultra_ball"]:
            ball = [b for b in self.inventory if b["name"] == "ultra_ball"][0]
            if ball["amount"] > 20:
                return
        if self.cash >= 20000:
            self.buy_item("ultra_ball", 20, True)
        if self.cash >= 10000:
            self.buy_item("ultra_ball", 10, True)


if __name__ == "__main__":
    pokeCommu = PokeCommu()
    for pokemon in pokeCommu.pokemons:
        # if "unown" in pokemon["name"]:
        #     print(pokemon)
        if "mime" in pokemon["name"]:
            print(pokemon)
