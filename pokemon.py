import requests
from unidecode import unidecode

from pokemonDB import PokemonDB, TypeDB


class Pokemon:
    db = PokemonDB()
    type_db = TypeDB()
    api_url = "https://tyradex.vercel.app/api/v1/pokemon/"

    def __init__(
        self,
        name_fr: str = None,
        name_en: str = None,
        id: int = 0,
        reg_form: str = None,
        spe_form: str = None,
        pcg: bool = False,
    ):
        self.fr_name = name_fr
        self.en_name = name_en
        self.id = id

        self.reg_form = reg_form
        self.spe_form = spe_form
        self.pcg = pcg

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

        if self.reg_form:
            name = f"{self.reg_form} {name}"
        if self.spe_form:
            name = f"{name} ({self.spe_form})"

        name = name.title()

        if self.pcg:
            name = f"PCG {name}"

        return name

    def __get_pokemon(self):
        if not self.id == 0:
            pokemon = self.__get_pokemon_data_id()
        elif self.fr_name is not None:
            pokemon = self.__get_pokemon_data("fr")
        elif self.en_name is not None:
            pokemon = self.__get_pokemon_data("en")
        else:
            pokemon = None

        if pokemon:
            self.id = pokemon["id"]
            self.fr_name = pokemon["name_fr"]
            self.en_name = pokemon["name_en"]

            self.stats = pokemon["stats"]
            self.height = pokemon["height"]
            self.weight = pokemon["weight"]

            self.fr_types = pokemon["types"]

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

        pokemon = self.db.get_pokemon(pokemon_name, lang)

        if pokemon:
            return pokemon
        else:
            pokemon_name = unidecode(pokemon_name)
            return self.__get_pokemon_from_api(pokemon_name)

    def __get_pokemon_data_id(self):
        pokemon = self.db.get_pokemon_id(self.id)

        if pokemon:
            return pokemon

        else:
            return self.__get_pokemon_from_api(str(self.id))

    def __get_pokemon_from_api(self, pokemon_name):
        print(f"Fetch data from the API for {pokemon_name}")

        pokemon_name = pokemon_name.replace(" ", "")
        response = requests.get(self.api_url + pokemon_name)

        print("Pokemon fetched")
        if response.status_code == 200:
            return self.__save_pokemon(response.json())
        else:
            return None

    def __save_pokemon(self, pokemon_data):
        name_fr = pokemon_data["name"]["fr"].replace("♀", "-f").replace("♂", "-m")
        name_en = pokemon_data["name"]["en"].replace("♀", "-f").replace("♂", "-m")

        height = float(pokemon_data["height"].replace(" m", "").replace(",", "."))
        weight = float(pokemon_data["weight"].replace(" kg", "").replace(",", "."))

        types = [unidecode(type["name"]) for type in pokemon_data["types"]]

        pokemon = {
            "id": int(pokemon_data["pokedex_id"]),
            "name_fr": name_fr,
            "name_en": name_en,
            "types": types,
            "stats": pokemon_data["stats"],
            "height": height,
            "weight": weight,
        }
        self.db.save_pokemon(pokemon)
        return pokemon
