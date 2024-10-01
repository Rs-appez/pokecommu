

from pokeCommu import PokeCommu
from pokemonData import PokemonData


class PokeBusiness():
    def __init__(self):
        self.pokemon_data = PokemonData()
        self.pokeCommu = PokeCommu()

    def catch_pokemon(self, pokemon):

        poke_data = self.pokemon_data.get_pokemon_data(pokemon)

        if poke_data:
            ball = self.find_best_ball(poke_data)
            if ball:
                return ball
            else:
                return None
            


    def find_best_ball(self, poke_data):
        best_ball = None
        balls = self.pokeCommu.inventory

        balls.index()

        pass