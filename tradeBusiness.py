from pokeCommu import PokeCommu
from pokemonData import PokemonData
from pokemon import Pokemon

from typing import List


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
        base=False,
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
        print("pokemon : ", pokemon)

        return
        if pokemon:
            poke_data = self.pokeCommu.trade_pokemon(pokemon["id"])
            if poke_data:
                print(
                    f"GET : {poke_data['name']} id {poke_data['id']} lvl {poke_data['lvl']} avgIV {poke_data['avgIV']}"
                )
            else:
                print("Trade failed")
        else:
            print("No pokemon to trade")

    def __find_pokemon_to_trade(self):
        # select selector
        selector = "avgIV"

        if self.level:
            selector = "lvl"
        if self.speed:
            selector = "speed"
        if self.defSpe:
            selector = "special_defense"
        if self.defense:
            selector = "defense"
        if self.hp:
            selector = "hp"
        if self.bst:
            selector = "baseStats"

        # sort order
        if self.sort == "gt":
            reverse = True
        else:
            reverse = False

        duplicated_pokemon = self.__get_first_duplicated_pokemon()

        if duplicated_pokemon:
            pokemons_to_trade = self.__get_all_pokemons_by_id(
                duplicated_pokemon["pokedexId"]
            )
            pokemons_to_trade = [pokemon for pokemon in pokemons_to_trade]
            pokemons_to_trade.sort(
                key=lambda x: (x["avgIV"], x[selector] if not reverse else -x[selector])
            )
            pokemon_to_trade = pokemons_to_trade[0]

            print(
                f"Trading {pokemon_to_trad['name']} lvl {pokemon_to_trade['lvl']} avgIV {pokemon_to_trade['avgIV']} id {pokemon_to_trade['id']}"
            )

            return pokemon_to_trade

    def __get_first_duplicated_pokemon(self):
        seen = set()
        for pokemon in self.pokeCommu.pokemons:
            id = pokemon.get("pokedexId")
            order = pokemon.get("order")
            data = self.pokemon_data.get_pokemon(order, "num")

            if id in seen:
                return pokemon
            if data:
                # check type
                if self.poke_type:
                    if not data.has_type(self.poke_type):
                        continue

                # check level
                if self.level:
                    if self.sort == "gt":
                        if not pokemon.get("lvl") > int(self.level):
                            continue
                    else:
                        if not pokemon.get("lvl") < int(self.level):
                            continue
                # check speed
                if self.speed:
                    if self.base:
                        stat = data.stats["speed"]
                    else:
                        stat = pokemon.get("speed")

                    if self.sort == "gt":
                        if stat <= int(self.speed):
                            continue
                    else:
                        if stat >= int(self.speed):
                            continue
                # check defense
                if self.defense:
                    if self.base:
                        stat = data.stats["def"]
                    else:
                        stat = pokemon.get("defense")

                    if self.sort == "gt":
                        if stat <= int(self.defense):
                            continue
                    else:
                        if stat >= int(self.defense):
                            continue
                # check special defense
                if self.defSpe:
                    if self.base:
                        stat = data.stats["spe_def"]
                    else:
                        stat = pokemon.get("special_defense")

                    if self.sort == "gt":
                        if stat <= int(self.defSpe):
                            continue
                    else:
                        if stat >= int(self.defSpe):
                            continue
                # check hp
                if self.hp:
                    if self.base:
                        stat = data.stats["hp"]
                    else:
                        stat = pokemon.get("hp")

                    if self.sort == "gt":
                        if stat <= int(self.hp):
                            continue
                    else:
                        if stat >= int(self.hp):
                            continue
                # check bst
                if self.bst:
                    stat = pokemon.get("baseStats")
                    if self.sort == "gt":
                        if stat <= int(self.bst):
                            continue
                    else:
                        if stat >= int(self.bst):
                            continue

            seen.add(id)
        return None

    def __get_all_pokemons_by_id(self, id) -> List[Pokemon]:
        return [
            pokemon
            for pokemon in self.pokeCommu.pokemons
            if pokemon.get("pokedexId") == id
        ]

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

            if id in duplicated_pokemons:
                if id in valid_pokemons:
                    return pokemon_ids[id]

            if data:
                if id not in duplicated_pokemons:
                    duplicated_pokemons.add(id)

                if self.__is_pokemon_valid(pokemon, data):
                    valid_pokemons.add(id)
                    pokemon_ids[id] = pokemon

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
            if self.base:
                stat = data.stats["weight"]
            else:
                stat = pokemon.get("weight")

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
