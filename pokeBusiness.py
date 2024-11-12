from pokeCommu import PokeCommu
from pokemonData import PokemonData
import asyncio
import random

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

        pokemons = self.pokeCommu.pokemons
        pokemons_shiny = self.pokeCommu.pokemons_shiny



        # Check if the pokemon is already caught
        if [poke for poke in pokemons if poke['name'] == poke_data['name_en']]:
            # Check if the pokemon is shiny
            if not [poke for poke in pokemons_shiny if poke['name'] == poke_data['name_en']]:
                if self.__check_ball_in_inventary('cherish_ball'):
                    best_ball = 'cherishball'
                    self.__wait()
                    return best_ball
            
            if self.__check_ball_in_inventary('repeat_ball'):
                best_ball = 'repeatball'
                self.__wait()
                return best_ball

        if self.__check_ball_in_inventary('quick_ball'):
            best_ball = 'quickball'
            self.__wait(random.randint(1, 5))
            return best_ball
        
        if self.__check_ball_in_inventary('timer_ball'):
            best_ball = 'timerball'
            self.__wait(80)
            return best_ball
    
        if poke_data['weight'] > 204.8:
            if self.__check_ball_in_inventary('heavy_ball'):
                best_ball = 'heavyball'
                self.__wait()
                return best_ball
            
        if poke_data['weight'] <= 9.9:
            if self.__check_ball_in_inventary('feather_ball'):
                best_ball = 'featherball'
                self.__wait()
                return best_ball
        
        # Check type ball
        types = [type for type in poke_data['types']]

        # 80%
        if 'Ice' in types:
            if self.__check_ball_in_inventary('frozen_ball'):
                best_ball = 'frozenball'
                self.__wait()
                return best_ball
            
        if 'Dark' in types:
            if self.__check_ball_in_inventary('night_ball'):
                best_ball = 'nightball'
                self.__wait()
                return best_ball
            
        if 'Ghost' in types:
            if self.__check_ball_in_inventary('phantom_ball'):
                best_ball = 'phantomball'
                self.__wait()
                return best_ball
            
        # 80% with stats
        stats = poke_data['stats']

        if stats['vit'] > 100:
            if self.__check_ball_in_inventary('fast_ball'):
                best_ball = 'fastball'
                self.__wait()
                return best_ball
            
        if stats['hp'] > 100:
            if self.__check_ball_in_inventary('heal_ball'):
                best_ball = 'healball'
                self.__wait()
                return best_ball
            
        
        if self.__check_ball_in_inventary('ultra_ball'):
            best_ball = 'ultraball'
            self.__wait()
            return best_ball

        # 70%

        if any(t in types for t in ['Poison', 'Psychic']):
            if self.__check_ball_in_inventary('cipher_ball'):
                best_ball = 'cipherball'
                self.__wait()
                return best_ball
    
        if any(t in types for t in ['Steel', 'Electric']):
            if self.__check_ball_in_inventary('magnet_ball'):
                best_ball = 'magnetball'
                self.__wait()
                return best_ball
        
        if any(t in types for t in ['Water', 'Bug']):
            if self.__check_ball_in_inventary('net_ball'):
                best_ball = 'netball'
                self.__wait()
                return best_ball
            
        # 55%
        if self.__check_ball_in_inventary('great_ball'):
            best_ball = 'greatball'
            self.__wait()
            return best_ball
        
        if self.__check_ball_in_inventary('stone_ball'):
            best_ball = 'stoneball'
            self.__wait()
            return best_ball
        
        if self.__check_ball_in_inventary('luxury_ball'):
            best_ball = 'luxuryball'
            self.__wait()
            return best_ball

        # 40%
        if self.__check_ball_in_inventary('level_ball'):
            best_ball = 'levelball'
            self.__wait()
            return best_ball

        # 30%
        if self.__check_ball_in_inventary('clone_ball'):
            best_ball = 'cloneball'
            self.__wait()
            return best_ball
        
        if self.__check_ball_in_inventary('poke_ball'):
            best_ball = 'pokeball'
            self.__wait()
            return best_ball
        
        if self.__check_ball_in_inventary('premier_ball'):
            best_ball = 'premierball'
            self.__wait()
            return best_ball
        
        return best_ball


    def __check_ball_in_inventary(self, ball):

        balls = self.pokeCommu.inventory

        if [b for b in balls if b['sprite_name'] == ball]:
            ball = [b for b in balls if b['sprite_name'] == ball][0]
            if ball['amount'] > 0:
                ball['amount'] -= 1
                return True

        return False
    
    def __wait(self, time : int = None):

        if not time:
            time = random.randint(5, 80)

        asyncio.run(self.__wait_coroutine(time))


    async def __wait_coroutine(self, time : int):
        await asyncio.sleep(time)
        return True