from pokeCommu import PokeCommu
from pokemonData import PokemonData
from ballBusiness import BallBusiness

import random


class PokeBusiness:
    def __init__(
        self,
        catch_all=True,
        poke_type=None,
        ball_type=None,
        partial=False,
        special=False,
    ):
        self.catch_all = catch_all
        self.poke_type = poke_type
        self.ball_type = ball_type
        self.partial = partial
        self.special = special
        self.is_partial = False
        self.pokemon_data = PokemonData()
        self.pokeCommu = PokeCommu()
        self.ballBusiness = BallBusiness(self.pokeCommu)

    def catch_pokemon(self, pokemon, priority=False):
        poke_data = self.pokemon_data.get_pokemon(pokemon, "en")

        print(f"Priority : {priority}")

        if poke_data:
            is_in_inventory = self.pokeCommu.is_pokemon_in_inventory(poke_data)

            # sometime bypass if partial is set
            if self.partial:
                if random.randint(0, 100) < 33:
                    print(f"Partial catch {poke_data.en_name}")
                    self.is_partial = True

            # Check if the pokemon is already caught when not catching all
            if (
                not self.catch_all
                and not self.is_partial
                and not (priority and self.special)
            ):
                if self.poke_type:
                    if not poke_data.has_type(self.poke_type) and is_in_inventory:
                        print(f"{poke_data.en_name} is not {self.poke_type}")
                        return None

                elif is_in_inventory:
                    print(f"{poke_data.en_name} already caught")
                    return None

            self.is_partial = False

            use_custom_ball = (
                self.ball_type
                and self.ballBusiness.check_ball_in_inventary(f"{self.ball_type}_ball")
                and not (priority and self.special)
            )
            print("use_custom_ball : ", use_custom_ball)

            use_best_ball = not use_custom_ball or not is_in_inventory
            print("use_best_ball : ", use_best_ball)

            ball = (
                self.ballBusiness.find_best_ball(poke_data)
                if use_best_ball
                else f"{self.ball_type}ball"
            )
            if not use_best_ball:
                self.ballBusiness.wait()

            print("ball : ", ball)

            if ball:
                return ball
            else:
                return None

    def auto_trade(
        self,
        poke_type=None,
        level=None,
        speed=None,
        sort=None,
        hp=None,
        bst=None,
        defSpe=None,
        base=None,
    ):
        pokemon = self.__find_pokemon_to_trade(
            poke_type=poke_type,
            level=level,
            speed=speed,
            sort=sort,
            defSpe=defSpe,
            hp=hp,
            bst=bst,
            base=base,
        )
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

    def __get_first_duplicated_pokemon(
        self,
        poke_type=None,
        level=None,
        speed=None,
        defSpe=None,
        hp=None,
        bst=None,
        sort=None,
        base=False,
    ):
        seen = set()
        for pokemon in self.pokeCommu.pokemons:
            id = pokemon.get("pokedexId")
            order = pokemon.get("order")
            data = self.pokemon_data.get_pokemon(order, "num")

            if id in seen:
                return pokemon
            if data:
                # check type
                if poke_type:
                    if not data.has_type(poke_type):
                        continue

                # check level
                if level:
                    if sort == "gt":
                        if not pokemon.get("lvl") > int(level):
                            continue
                    else:
                        if not pokemon.get("lvl") < int(level):
                            continue
                # check speed
                if speed:
                    if sort == "gt":
                        if not pokemon.get("speed") >= int(speed):
                            continue
                    else:
                        if not pokemon.get("speed") <= int(speed):
                            continue
                # check special defense
                if defSpe:
                    if base:
                        stat = data.stats["spe_def"]
                    else:
                        stat = pokemon.get("special_defense")

                    if sort == "gt":
                        if stat <= int(defSpe):
                            continue
                    else:
                        if stat >= int(defSpe):
                            continue
                # check hp
                if hp:
                    if base:
                        stat = data.stats["hp"]
                    else:
                        stat = pokemon.get("hp")

                    if sort == "gt":
                        if stat <= int(hp):
                            continue
                    else:
                        if stat >= int(hp):
                            continue
                # check bst
                if bst:
                    stat = pokemon.get("baseStats")
                    if sort == "gt":
                        if stat <= int(bst):
                            continue
                    else:
                        if stat >= int(bst):
                            continue

            seen.add(id)
        return None

    def __find_pokemon_to_trade(
        self,
        poke_type=None,
        level=None,
        speed=None,
        sort=None,
        hp=None,
        bst=None,
        defSpe=None,
        base=None,
        selector="",
    ):
        # select selector
        if level:
            selector = "lvl"
        if speed:
            selector = "speed"
        if defSpe:
            selector = "special_defense"
        if hp:
            selector = "hp"
        if bst:
            selector = "baseStats"

        if not selector:
            selector = "avgIV"

        # sort order
        if sort == "gt":
            reverse = True
        else:
            reverse = False

        duplicated_pokemon = self.__get_first_duplicated_pokemon(
            poke_type=poke_type,
            level=level,
            speed=speed,
            defSpe=defSpe,
            hp=hp,
            bst=bst,
            sort=sort,
            base=base,
        )

        if duplicated_pokemon:
            pokemons_to_trade = self.__get_all_pokemons_by_id(
                duplicated_pokemon["pokedexId"]
            )
            pokemons_to_trade = [
                pokemon for pokemon in pokemons_to_trade if not pokemon["locked"]
            ]
            pokemons_to_trade.sort(key=lambda x: x[selector], reverse=reverse)

            print(
                f"Trading {pokemons_to_trade[0]['name']} lvl {pokemons_to_trade[0]['lvl']} avgIV {pokemons_to_trade[0]['avgIV']} id {pokemons_to_trade[0]['id']}"
            )

            return pokemons_to_trade[0]

    def __get_all_pokemons_by_id(self, id):
        return [
            pokemon
            for pokemon in self.pokeCommu.pokemons
            if pokemon.get("pokedexId") == id
        ]
