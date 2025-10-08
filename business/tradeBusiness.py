from pokeCommu import PokeCommu
from models.pokemonData import PokemonData
from models.pokemon import Pokemon


class TradeBusiness:
    def __init__(
        self,
        poke_type: str = None,
        level: int = None,
        speed: int = None,
        greater: bool = True,
        hp: int = None,
        weight: float = None,
        bst: int = None,
        defense: int = None,
        defSpe: int = None,
        base: bool = False,
    ):
        self.poke_type = poke_type
        self.level = level
        self.speed = speed
        self.greater = greater
        self.hp = hp
        self.weight = weight
        self.bst = bst
        self.defense = defense
        self.defSpe = defSpe
        self.base = base

        self.pokemon_data = PokemonData()
        self.pokeCommu = PokeCommu()

    def auto_trade(self):
        pokemon = self.__get_pokemon_to_trade()

        if pokemon and self.__trade_allowed(pokemon):
            poke_data = self.pokeCommu.trade_pokemon(pokemon["id"])
            if poke_data:
                print(
                    f"TRADED : {pokemon['name']} id {pokemon['id']} lvl {
                        pokemon['lvl']
                    } avgIV {pokemon['avgIV']}"
                )
                print(
                    f"GET : {poke_data['name']} id {poke_data['id']} lvl {
                        poke_data['lvl']
                    } avgIV {poke_data['avgIV']}"
                )
            else:
                print("Trade failed")
        else:
            print("No pokemon to trade")

    def __get_pokemon_to_trade(self) -> dict:
        pokemons = self.pokeCommu.pokemons
        pokemons.sort(key=lambda p: (p["baseStats"], p["avgIV"]))

        duplicated_pokemons = set()
        valid_pokemons = set()
        pokemon_ids = {}

        for pokemon in pokemons:
            id = pokemon.get("pokedexId")
            order = pokemon.get("order")
            data = self.pokemon_data.get_pokemon(order, "num")

            if id in duplicated_pokemons and id in valid_pokemons:
                return pokemon_ids[id]

            if data:
                if self.__is_pokemon_valid(pokemon, data):
                    valid_pokemons.add(id)
                    pokemon_ids[id] = pokemon

                if id not in duplicated_pokemons:
                    duplicated_pokemons.add(id)

                elif id in valid_pokemons:
                    return pokemon_ids[id]

    def __is_pokemon_valid(self, pokemon: dict, data: Pokemon) -> bool:
        if self.poke_type and not data.has_type(self.poke_type):
            return False

        if self.level:
            stat = pokemon.get("lvl")
            if self.greater:
                if stat <= self.level:
                    return False
            else:
                if stat >= self.level:
                    return False

        if self.speed:
            if self.base:
                stat = data.stats["speed"]
            else:
                stat = pokemon.get("speed")

            if self.greater:
                if stat <= self.speed:
                    return False
            else:
                if stat >= self.speed:
                    return False

        if self.defense:
            if self.base:
                stat = data.stats["def"]
            else:
                stat = pokemon.get("defense")

            if self.greater:
                if stat <= self.defense:
                    return False
            else:
                if stat >= self.defense:
                    return False

        if self.defSpe:
            if self.base:
                stat = data.stats["spe_def"]
            else:
                stat = pokemon.get("special_defense")

            if self.greater:
                if stat <= self.defSpe:
                    return False
            else:
                if stat >= self.defSpe:
                    return False

        if self.hp:
            if self.base:
                stat = data.stats["hp"]
            else:
                stat = pokemon.get("hp")

            if self.greater:
                if stat <= self.hp:
                    return False
            else:
                if stat >= self.hp:
                    return False

        if self.weight:
            stat = data.weight
            if self.greater:
                if stat <= self.weight:
                    return False
            else:
                if stat >= self.weight:
                    return False

        if self.bst:
            stat = pokemon.get("baseStats")
            if self.greater:
                if stat <= self.bst:
                    return False
            else:
                if stat >= self.bst:
                    return False
        return True

    def __trade_allowed(self, pokemon: dict) -> bool:
        poke = self.pokeCommu.get_pokemon(pokemon["id"])
        if poke:
            if poke.get("tradable") is not None:
                print("You are on cooldown !")
                return False
        return True
