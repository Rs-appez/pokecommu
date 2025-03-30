import asyncio
import random

from pokeCommu import PokeCommu


class BallBusiness:
    def __init__(self, pokeCommu: PokeCommu):
        self.inventory = pokeCommu.inventory
        self.pokemons = pokeCommu.pokemons
        self.shinies = pokeCommu.shinies

    def find_best_ball(self, pokemon):
        # Check if the pokemon is already caught
        if any(poke["name"] == pokemon.en_name for poke in self.pokemons):
            if not any(poke["name"] == pokemon.en_name for poke in self.shinies):
                if best_ball := self.__check_cherish_ball():
                    return best_ball
            if best_ball := self.__check_drop_ball():
                return best_ball
            if best_ball := self.__check_duplicate_ball():
                return best_ball

        checks = [
            self.__check_time_ball,
            lambda: self.__check_weight_ball(pokemon.weight),
            lambda: self.__check_type_ball(pokemon.en_types),
            lambda: self.__check_stats_ball(pokemon.stats),
            self.__check_ultra_ball,
            self.__check_drop_ball,
            self.__check_low_ball,
        ]

        for check in checks:
            if best_ball := check():
                return best_ball

        return None

    def check_ball_in_inventary(self, ball):
        if [b for b in self.inventory if b["sprite_name"] == ball]:
            ball = [b for b in self.inventory if b["sprite_name"] == ball][0]
            if ball["amount"] > 0:
                ball["amount"] -= 1
                return True

        return False

    def __check_cherish_ball(self):
        # 80%
        if self.check_ball_in_inventary("ultra_cherish_ball"):
            best_ball = "ultracherishball"
            self.__wait()
            return best_ball
        # 55%
        if self.check_ball_in_inventary("great_cherish_ball"):
            best_ball = "greatcherishball"
            self.__wait()
            return best_ball
        # 30%
        if self.check_ball_in_inventary("cherish_ball"):
            best_ball = "cherishball"
            self.__wait()
            return best_ball
        return None

    def __check_drop_ball(self):
        # 55%
        if self.check_ball_in_inventary("stone_ball"):
            best_ball = "stoneball"
            self.__wait()
            return best_ball
        return None

    def __check_duplicate_ball(self):
        if self.check_ball_in_inventary("repeat_ball"):
            best_ball = "repeatball"
            self.__wait()
            return best_ball
        return None

    def __check_time_ball(self):
        if self.check_ball_in_inventary("quick_ball"):
            best_ball = "quickball"
            self.__wait(random.randint(1, 5))
            return best_ball

        if self.check_ball_in_inventary("timer_ball"):
            best_ball = "timerball"
            self.__wait(random.randint(1, 5))
            self.__wait(70)
            return best_ball
        return None

    def __check_weight_ball(self, weight):
        if weight > 204.8:
            if self.check_ball_in_inventary("heavy_ball"):
                best_ball = "heavyball"
                self.__wait()
                return best_ball

        if weight <= 9.9:
            if self.check_ball_in_inventary("feather_ball"):
                best_ball = "featherball"
                self.__wait()
                return best_ball
        return None

    def __check_type_ball(self, types):
        type_ball_mapping = {
            "Ice": "frozen_ball",
            "Normal": "basic_ball",
            "Dark": "night_ball",
            "Ghost": "phantom_ball",
            "Flying": "mach_ball",
            "Fighting": "mach_ball",
            "Poison": "cipher_ball",
            "Psychic": "cipher_ball",
            "Steel": "magnet_ball",
            "Electric": "magnet_ball",
            "Fairy": "fantasy_ball",
            "Dragon": "fantasy_ball",
            "Fire": "sun_ball",
            "Grass": "sun_ball",
            "Water": "net_ball",
            "Bug": "net_ball",
            "Rock": "geo_ball",
            "Ground": "geo_ball",
        }

        for t in types:
            if ball := type_ball_mapping.get(t):
                if self.check_ball_in_inventary(ball):
                    best_ball = ball.replace("_ball", "ball")
                    self.__wait()
                    return best_ball

        return None

    def __check_stats_ball(self, stats):
        if stats["vit"] > 100:
            if self.check_ball_in_inventary("fast_ball"):
                best_ball = "fastball"
                self.__wait()
                return best_ball

        if stats["hp"] > 100:
            if self.check_ball_in_inventary("heal_ball"):
                best_ball = "healball"
                self.__wait()
                return best_ball

        return None

    def __check_ultra_ball(self):
        if self.check_ball_in_inventary("ultra_ball"):
            best_ball = "ultraball"
            self.__wait()
            return best_ball
        return None

    def __check_low_ball(self):
        # 55%
        if self.check_ball_in_inventary("great_ball"):
            best_ball = "greatball"
            self.__wait()
            return best_ball

        if self.check_ball_in_inventary("luxury_ball"):
            best_ball = "luxuryball"
            self.__wait()
            return best_ball

        # 40%
        if self.check_ball_in_inventary("level_ball"):
            best_ball = "levelball"
            self.__wait()
            return best_ball

        # 30%
        if self.check_ball_in_inventary("clone_ball"):
            best_ball = "cloneball"
            self.__wait()
            return best_ball

        if self.check_ball_in_inventary("poke_ball"):
            best_ball = " "
            self.__wait()
            return best_ball

        if self.check_ball_in_inventary("premier_ball"):
            best_ball = " "
            self.__wait()
            return best_ball
        return None

    def __wait(self, time: int = 0):
        if not time:
            time = random.randint(5, 80)

        asyncio.run(self.__wait_coroutine(time))

    async def __wait_coroutine(self, time: int):
        await asyncio.sleep(time)
        return True
