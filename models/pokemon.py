#!venv/bin/python3
import requests
from unidecode import unidecode

from db.pokemonDB import PokemonDB, TypeDB


class Pokemon:
    db = PokemonDB()
    type_db = TypeDB()
    api_url = "https://tyradex.app/api/v1/pokemon/"

    def __init__(
        self,
        name_fr: str = None,
        name_en: str = None,
        id: int = 0,
        reg_form: str = None,
        spe_form: str = None,
        pcg: bool = False,
    ):
        if not any([name_fr, name_en, id]):
            raise ValueError("At least one of name_fr, name_en or id must be provided")

        self.fr_name = name_fr
        self.en_name = name_en
        self.id = id
        self.db_id = None

        self.reg_form = reg_form
        self.spe_form = spe_form
        self.pcg: bool = pcg

        self.tier = None
        self.generation = 0
        self.fr_types = []
        self.en_types = []
        self.stats = []
        self.height = 0
        self.weight = 0

        self.__get_pokemon()

    def __str__(self):
        return f"{self.id} - {self.get_pcg_name()}"

    def has_type(self, type_name):
        types = map(str.lower, self.en_types + self.fr_types)
        return type_name.lower() in types

    def get_pcg_name(self) -> str:
        name = self.en_name
        name = (
            name.replace("'", "")
            .replace("’", "")
            .replace(".", "")
            .replace(" ", "-")
            .replace("é", "e")
            .replace("è", "e")
            .replace("ê", "e")
        )

        if self.reg_form:
            name = f"{name}-{self.reg_form}"
        if self.spe_form:
            name = f"{name}-{self.spe_form}"
        if self.pcg:
            name = f"{name}-pcg"

        return name.lower()

    def __get_pokemon(self):
        if not self.id == 0:
            pokemon_data = self.__get_pokemon_data_id()
        elif self.fr_name is not None:
            pokemon_data = self.__get_pokemon_data("fr")
        elif self.en_name is not None:
            pokemon_data = self.__get_pokemon_data("en")
        else:
            pokemon_data = None

        if pokemon_data:
            self.id = pokemon_data["pokemon_id"]
            self.db_id = pokemon_data["id"]
            self.fr_name = pokemon_data["name_fr"]
            self.en_name = pokemon_data["name_en"]

            self.generation = pokemon_data["generation"]
            self.stats = pokemon_data["stats"]
            self.height = pokemon_data["height"]
            self.weight = pokemon_data["weight"]
            self.tier = pokemon_data.get("tier", None)

            self.fr_types = pokemon_data["types"]

            for type in self.fr_types:
                type_data = self.type_db.get_type(type)
                if type_data:
                    self.en_types.append(type_data["name_en"])

    def __get_pokemon_data(self, lang):
        if lang == "fr":
            pokemon_name = self.fr_name
        elif lang == "en":
            pokemon_name = self.en_name
        else:
            return

        pokemon_name = pokemon_name.replace("♀", "-f").replace("♂", "-m")
        pokemon_name = pokemon_name.replace("’", "'")

        pokemon_data = self.db.get_pokemon(pokemon_name, lang, self.reg_form)

        if pokemon_data:
            return pokemon_data
        else:
            pokemon_name = unidecode(pokemon_name)
            return self.__get_pokemon_from_api(pokemon_name)

    def __get_pokemon_data_id(self) -> dict | None:
        pokemon_data = self.db.get_pokemon_id(self.id, self.reg_form)

        if pokemon_data:
            return pokemon_data

        else:
            return self.__get_pokemon_from_api(str(self.id))

    def __get_pokemon_from_api(self, pokemon_name):
        print(f"Fetch data from the API for {self.reg_form or ''} {pokemon_name}")

        pokemon_name = pokemon_name.replace(" ", "")
        url = self.api_url + pokemon_name
        if self.reg_form:
            url += f"/{self.reg_form}"

        response = requests.get(url)

        print("Pokemon fetched")
        if response.status_code == 200:
            pokemon = response.json()
            if self.reg_form:
                pokemon["name"]["fr"], pokemon["name"]["en"] = self.__get_clean_name(
                    pokemon["pokedex_id"]
                )
            return self.__save_pokemon(pokemon, self.reg_form)
        else:
            return None

    def __get_clean_name(self, id: int) -> tuple[str, str]:
        normal_region = Pokemon(id=id)
        return (normal_region.fr_name, normal_region.en_name)

    def __save_pokemon(self, pokemon_data, region=None):
        name_fr = pokemon_data["name"]["fr"].replace("♀", "-f").replace("♂", "-m")
        name_en = pokemon_data["name"]["en"].replace("♀", "-f").replace("♂", "-m")

        height = float(pokemon_data["height"].replace(" m", "").replace(",", "."))
        weight = float(pokemon_data["weight"].replace(" kg", "").replace(",", "."))

        types = [unidecode(type["name"]) for type in pokemon_data["types"]]

        pokemon = {
            "pokemon_id": int(pokemon_data["pokedex_id"]),
            "region": region,
            "generation": int(pokemon_data["generation"]),
            "name_fr": name_fr,
            "name_en": name_en,
            "types": types,
            "stats": pokemon_data["stats"],
            "height": height,
            "weight": weight,
        }
        pokemon["id"] = self.db.save_pokemon(pokemon)
        return pokemon

    def save_tier(self, tier: str):
        print(f"Saving tier '{tier}' for Pokemon {self.en_name}")
        self.tier = tier
        self.db.update_pokemon_tier(self.db_id, tier)


if __name__ == "__main__":
    pokemon_id = 5
    pokemon = Pokemon(id=pokemon_id)

    if pokemon.id == 0:
        print(f"Pokemon '{pokemon_id}' not found.")
    else:
        print(f"Pokemon found: {pokemon}")
        print(
            f"ID: {pokemon.id}, Generation: {pokemon.generation}, Types: {
                pokemon.fr_types
            }, Stats: {pokemon.stats}, Height: {pokemon.height}, Weight: {
                pokemon.weight
            }"
        )

    pokemon_name = "Pikachu"
    pokemon = Pokemon(name_en=pokemon_name)

    print(f"Pokemon found: {pokemon}")
