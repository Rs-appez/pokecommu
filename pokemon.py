import requests
from unidecode import unidecode

from pokemonDB import PokemonDB, TypeDB


class Pokemon:

    db = PokemonDB()
    type_db = TypeDB()
    api_url = "https://tyradex.vercel.app/api/v1/pokemon/"

    def __init__(self, name_fr=None, name_en=None, id=0):

        self.fr_name = name_fr
        self.en_name = name_en
        self.id = id

        self.fr_types = []
        self.en_types = []
        self.stats = []
        self.height = 0
        self.weight = 0

        self.__get_pokemon()

    def __get_pokemon(self):

        if not self.id == 0:
            pokemon = self.__get_pokemon_data_id()
        elif self.fr_name != None or self.en_name != None:
            pokemon = self.__get_pokemon_data()
        else:
            pokemon = None

        if pokemon:

            self.stats = pokemon["stats"]
            self.height = pokemon["height"]
            self.weight = pokemon["weight"]

            self.fr_types = pokemon["types"]

            for type in self.fr_types:
                type_en = self.type_db.get_type(type)
                if type_en:
                    self.en_types.append(type_en)

    def __get_pokemon_data(self):

        pokemon_name = self.fr_name if self.fr_name else self.en_name

        if not pokemon_name:
            return

        pokemon_name = unidecode(
            pokemon_name.replace("♀", "-f").replace("♂", "-m")
        ).lower()

        pokemon = self.db.get_pokemon(pokemon_name)

        if pokemon:
            return pokemon
        else:
            return self.__get_pokemon_from_api(pokemon_name)

    def __get_pokemon_data_id(self):

        pokemon = self.db.get_pokemon_id(id)

        if pokemon:
            return pokemon

        else:
            return self.__get_pokemon_from_api(str(id))

    def __get_pokemon_from_api(self, pokemon_name):

        print(f"Fetch data from the API for {pokemon_name}")
        response = requests.get(self.api_url + pokemon_name)
        print("Pokemon fetched")
        if response.status_code == 200:
            return self.__save_pokemon(response.json())
        else:
            return None

    def __save_pokemon(self, pokemon_data):

        name_fr = unidecode(
            pokemon_data["name"]["fr"].replace("♀", "-f").replace("♂", "-m")
        )

        height = float(pokemon_data["height"].replace(" m", "").replace(",", "."))
        weight = float(pokemon_data["weight"].replace(" kg", "").replace(",", "."))

        types = [unidecode(type["name"]) for type in pokemon_data["types"]]

        pokemon = {
            "id": int(pokemon_data["pokedex_id"]),
            "name_fr": name_fr,
            "name_en": pokemon_data["name"]["en"],
            "types": types,
            "stats": pokemon_data["stats"],
            "height": height,
            "weight": weight,
        }
        self.db.save_pokemon(pokemon)
        return pokemon
