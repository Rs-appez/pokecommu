from pokeCommu import PokeCommu
from pokemonData import PokemonData
from ballBusiness import BallBusiness
from pokemon import Pokemon

import random


class PokeBusiness:
    def __init__(
        self,
        catch_all=True,
        poke_type=None,
        poke_weight=None,
        poke_generation=None,
        greater=False,
        ball_type=None,
        partial=False,
        special=False,
    ):
        self.catch_all = catch_all
        self.poke_type = poke_type
        self.poke_weight = poke_weight
        self.poke_generation = poke_generation
        self.ball_type = ball_type
        self.greater = greater
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
            print(f"Pokemon in inventory : {is_in_inventory}")

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
                if not self.check_pokemon_stats(poke_data) and is_in_inventory:
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

    def check_pokemon_stats(self, pokemon: Pokemon) -> bool:
        if pokemon:
            if self.poke_type is not None:
                if pokemon.has_type(self.poke_type):
                    print(f"{pokemon.en_name} is {self.poke_type}")
                    return True
            if self.poke_weight is not None:
                if self.greater:
                    if pokemon.weight > self.poke_weight:
                        print(
                            f"{pokemon.en_name} weight is greather than {self.poke_weight}"
                        )
                        return True
                else:
                    if pokemon.weight < self.poke_weight:
                        print(
                            f"{pokemon.en_name} weight is lighter than {self.poke_weight}"
                        )
                        return True
            if self.poke_generation is not None:
                if pokemon.generation == self.poke_generation:
                    print(f"{pokemon.en_name} is from generation {self.poke_generation}")
                    return True
        return False
