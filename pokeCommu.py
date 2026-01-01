import json
import pickle
from itertools import chain
from threading import Lock

import requests
from decouple import config

from models.pokemon import Pokemon
from models.pokemonData import PokemonDataMapper


class PokeCommu:
    url = "https://poketwitch.bframework.de/api/game/ext/"

    url_trainer = url + "trainer/"
    url_shop = url + "shop/"

    url_poke = url_trainer + "pokemon/v2/"
    url_poke_v3 = url_trainer + "pokemon/v3/"
    url_inventory = url_trainer + "inventory/v3/"
    url_trade = url_trainer + "wonder-trade/"
    url_pokedex = url_trainer + "pokedex/v2/"

    url_purchase = url_shop + "purchase/"

    token = config("PCG_TOKEN")
    header = {"Authorization": token}

    exeptions_pokemons = []

    def __init__(self):
        self.pokemons = []
        self.pokemons_locked = []
        self.pokemons_shiny = []
        self.eggs = []
        self.pokedex = {}
        self.inventory = []

        self.poke_buddy: Pokemon | None = None

        self.cash = 0

        self.pokemon_lock = Lock()
        self.inventory_lock = Lock()
        self.pokedex_lock = Lock()

        self.refresh_all()

    def refresh_all(self):
        self.load_pokemons_pkl()
        self.load_inventory_pkl()
        self.load_pokedex_pkl()

    def save_all(self):
        self._save_pokemons()
        self._save_inventory()
        self._save_pokedex()

    def load_pokemon_api(self):
        response = requests.get(self.url_poke, headers=self.header)
        if response.status_code == 200:
            self.load_pokemons(response.json())
            return True
        else:
            print(f"Error loading pokemon: {response.json()}")
            return False

    def load_pokemon_json(self):
        with open("json/pokemons.json", "r") as file:
            pokemons = json.load(file)
            self.load_pokemons(pokemons)
            return True

    def load_pokemons_pkl(self):
        with self.pokemon_lock:
            try:
                with open("pkl/pokemons.pkl", "rb") as file:
                    self.pokemons = pickle.load(file)
                with open("pkl/pokemons_locked.pkl", "rb") as file:
                    self.pokemons_locked = pickle.load(file)
                with open("pkl/pokemons_shiny.pkl", "rb") as file:
                    self.pokemons_shiny = pickle.load(file)
                with open("pkl/eggs.pkl", "rb") as file:
                    self.eggs = pickle.load(file)
            except FileNotFoundError:
                self.pokemons = []
                self.pokemons_locked = []
                self.pokemons_shiny = []
                self.eggs = []

    def load_pokemons(self, pokemons_data: dict):
        with self.pokemon_lock:
            for pokemon in pokemons_data["allPokemon"]:
                if pokemon["isLoanPokemon"]:
                    continue
                pokemon["name"] = pokemon["name"].lower()
                if "egg" in pokemon["name"].split("-"):
                    self.eggs.append(pokemon)
                else:
                    if pokemon["isBuddy"]:
                        self.poke_buddy = PokemonDataMapper.get_pokemon_from_pcg(
                            pokemon
                        )
                        print(self.poke_buddy.en_types)
                    if pokemon["locked"]:
                        self.pokemons_locked.append(pokemon)
                    elif pokemon["isShiny"]:
                        self.pokemons_shiny.append(pokemon)
                    else:
                        self.pokemons.append(pokemon)

    def _save_pokemons(self):
        with open("pkl/pokemons.pkl", "wb") as file:
            pickle.dump(self.pokemons, file)
        with open("pkl/pokemons_locked.pkl", "wb") as file:
            pickle.dump(self.pokemons_locked, file)
        with open("pkl/pokemons_shiny.pkl", "wb") as file:
            pickle.dump(self.pokemons_shiny, file)
        with open("pkl/eggs.pkl", "wb") as file:
            pickle.dump(self.eggs, file)

    def load_inventory_api(self):
        response = requests.get(self.url_inventory, headers=self.header)
        print("response : ", response.status_code, response.text)
        if response.status_code == 200:
            json_response = response.json()
            self.load_inventory(json_response)
            return True
        else:
            return False

    def load_inventory_json(self):
        with open("json/inventory.json", "r") as file:
            inventory = json.load(file)
            self.load_inventory(inventory)
            return True

    def load_inventory_pkl(self):
        with self.inventory_lock:
            try:
                with open("pkl/inventory.pkl", "rb") as file:
                    self.inventory = pickle.load(file)
            except FileNotFoundError:
                self.inventory = []

    def load_inventory(self, inventory_data: dict):
        with self.inventory_lock:
            self.cash = inventory_data["cash"]
            for ball in inventory_data["allItems"]:
                if ball["type"] == 2:
                    self.inventory.append(ball)

    def _save_inventory(self):
        with open("pkl/inventory.pkl", "wb") as file:
            pickle.dump(self.inventory, file)

    def load_pokedex_api(self):
        response = requests.get(
            self.url_pokedex,
            headers=self.header,
        )
        if response.status_code == 200:
            pokedex_json = response.json()
            self.load_pokedex(pokedex_json)

            return True
        else:
            return False

    def load_pokedex_json(self):
        with open("json/pokedex.json", "r") as file:
            pokedex_json = json.load(file)
            self.load_pokedex(pokedex_json)

            return True

    def load_pokedex(self, pokedex_data: dict):
        with self.pokedex_lock:
            for pokemon in pokedex_data["dex"]:
                self.pokedex[pokemon["name"]] = pokemon["c"]

    def load_pokedex_pkl(self):
        with self.pokedex_lock:
            try:
                with open("pkl/pokedex.pkl", "rb") as file:
                    self.pokedex = pickle.load(file)
            except FileNotFoundError:
                self.pokedex = {}

    def _save_pokedex(self):
        with open("pkl/pokedex.pkl", "wb") as file:
            pickle.dump(self.pokedex, file)

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
        with self.pokemon_lock:
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

        response = requests.post(self.url_purchase, headers=self.header, data=data)

        if response.status_code == 200:
            print(f"Bought {amount} {item}")
            if refresh:
                self.load_inventory_api()
            return True
        return False

    def is_pokemon_in_inventory(self, pokemon: Pokemon) -> bool:
        with self.pokemon_lock:
            poke_name = pokemon.get_pcg_name()

            if poke_name in self.exeptions_pokemons:
                return False

            if any(
                poke["name"] == poke_name
                for poke in chain(
                    self.pokemons, self.pokemons_shiny, self.pokemons_locked
                )
            ):
                return True
            return False

    def is_pokemon_in_pokedex(self, pokemon: Pokemon) -> bool:
        with self.pokedex_lock:
            poke_name = pokemon.get_pcg_name()
            return self.pokedex.get(poke_name, False)

    def is_shiny_in_inventory(self, pokemon: Pokemon) -> bool:
        with self.pokemon_lock:
            poke_name = pokemon.get_pcg_name()

            if any(poke["name"] == poke_name for poke in self.pokemons_shiny):
                return True
            return False

    def check_ball_in_inventary(self, ball) -> bool:
        with self.inventory_lock:
            if [b for b in self.inventory if b["name"] == ball]:
                ball = [b for b in self.inventory if b["name"] == ball][0]
                if ball["amount"] > 0:
                    return True

            return False

    def remove_ball_from_inventory(self, ball) -> bool:
        with self.inventory_lock:
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
    pikachu = Pokemon(name_en="pikachu")
    vulpix_aloa = Pokemon(name_en="vulpix", reg_form="alola")
    vulpix = Pokemon(name_en="vulpix")

    print(pokeCommu.is_pokemon_in_pokedex(pikachu))
    print(pokeCommu.is_pokemon_in_pokedex(vulpix_aloa))
    print(pokeCommu.is_pokemon_in_pokedex(vulpix))

    # pokeCommu.load_inventory()
    # for pokemon in pokeCommu.pokemons:
    #     # if "unown" in pokemon["name"]:
    #     #     print(pokemon)
    #     if "mime" in pokemon["name"]:
    #         print(pokemon)
