from models.pokemonData import PokemonDataMapper
from pokeCommu import PokeCommu
from business.ballBusiness import BallBusiness
from models.pokemon import Pokemon
from utils.utils_colors import get_bool_color, reset_color, get_color, Color

import random


class PokeBusiness:
    def __init__(
        self,
        catch_all: bool = True,
        hard_pokedex: bool = False,
        poke_type: str = None,
        poke_weight: float = None,
        poke_generation: int = None,
        greater: bool = False,
        ball_type: str = None,
        partial: bool = False,
        special: bool = False,
    ):
        self.catch_all: bool = catch_all
        self.hard_pokedex: bool = hard_pokedex
        self.poke_type: str = poke_type
        self.poke_weight: float = poke_weight
        self.poke_generation: int = poke_generation
        self.ball_type: str = ball_type
        self.greater: bool = greater
        self.partial: bool = partial
        self.special: bool = special
        self.is_partial: bool = False
        self.pokeCommu: PokeCommu = PokeCommu()
        self.ballBusiness: BallBusiness = BallBusiness(self.pokeCommu, special)

    def catch_pokemon(self, pokemon_data, priority=False):
        pokemon: Pokemon = PokemonDataMapper.get_pokemon_from_chat(pokemon_data, "en")

        print(f"🌟 Priority 🌟 : {get_bool_color(priority)}{priority}{reset_color()}")

        if pokemon:
            is_in_inventary = self.pokeCommu.is_pokemon_in_inventory(pokemon)
            print(
                f"Pokemon in inventory : {get_bool_color(is_in_inventary)}{
                    is_in_inventary
                }{reset_color()}"
            )
            is_in_pokedex = self.pokeCommu.is_pokemon_in_pokedex(pokemon)
            print(
                f"Pokemon in pokedex : {get_bool_color(is_in_pokedex)}{is_in_pokedex}{
                    reset_color()
                }"
            )

            is_in_possession: bool = is_in_inventary and (
                is_in_pokedex or self.hard_pokedex
            )

            # sometime bypass if partial is set
            if self.partial:
                if random.randint(0, 100) < 33:
                    print(
                        f"{get_color(Color.MAGENTA)}Partial catch {pokemon.en_name}{
                            reset_color()
                        }"
                    )
                    self.is_partial = True

            # Check if the pokemon is already caught when not catching all
            if (
                not self.catch_all
                and not self.is_partial
                and not (priority and self.special)
            ):
                if not self.check_pokemon_stats(pokemon) and is_in_possession:
                    print(
                        f"{get_color(Color.GREEN)}{pokemon.en_name} already caught{
                            reset_color()
                        }"
                    )
                    return None

            self.is_partial = False

            use_custom_ball = (
                self.ball_type
                and self.ballBusiness.check_ball_in_inventary(f"{self.ball_type}_ball")
                and not (priority and self.special)
            )
            print(
                f"use_custom_ball : {get_bool_color(use_custom_ball)}{use_custom_ball}{
                    reset_color()
                }"
            )

            use_best_ball = not use_custom_ball or not is_in_possession
            print(
                f"use_best_ball : {get_bool_color(use_best_ball)}{use_best_ball}{reset_color()}"
            )

            ball = (
                self.ballBusiness.find_best_ball(pokemon)
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
                    print(
                        f"{pokemon.en_name} is from generation {self.poke_generation}"
                    )
                    return True
        return False
