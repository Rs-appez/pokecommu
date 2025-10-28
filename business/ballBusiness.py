import asyncio
import random

from pokeCommu import PokeCommu


class BallBusiness:
    def __init__(self, pokeCommu: PokeCommu, event: bool = False):
        self.pokeCommu = pokeCommu
        self.event = event

    def find_best_ball(self, pokemon):
        # Check if the pokemon is already caught
        if self.pokeCommu.is_pokemon_in_inventory(pokemon):
            if not self.pokeCommu.is_shiny_in_inventory(pokemon):
                if best_ball := self.__check_cherish_ball():
                    return best_ball
            if best_ball := self.__check_drop_ball():
                return best_ball
            if best_ball := self.__check_duplicate_ball():
                return best_ball

        checks = [
            lambda : self.__check_event_ball(pokemon.en_types),
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

    def check_ball_in_inventary(self, ball) -> bool:
        return self.pokeCommu.remove_ball_from_inventory(ball)

    def __check_cherish_ball(self):
        # 80%
        if self.check_ball_in_inventary("ultra_cherish_ball"):
            best_ball = "ultracherishball"
            self.wait()
            return best_ball
        # 55%
        if self.check_ball_in_inventary("great_cherish_ball"):
            best_ball = "greatcherishball"
            self.wait()
            return best_ball
        # 30%
        if self.check_ball_in_inventary("cherish_ball"):
            best_ball = "cherishball"
            self.wait()
            return best_ball
        return None

    def __check_drop_ball(self):
        # 55%
        if self.check_ball_in_inventary("stone_ball"):
            best_ball = "stoneball"
            self.wait()
            return best_ball
        return None

    def __check_duplicate_ball(self):
        if self.check_ball_in_inventary("repeat_ball"):
            best_ball = "repeatball"
            self.wait()
            return best_ball
        return None

    def __check_time_ball(self):
        if self.check_ball_in_inventary("quick_ball"):
            best_ball = "quickball"
            self.wait(random.randint(1, 5))
            return best_ball

        if self.check_ball_in_inventary("timer_ball"):
            best_ball = "timerball"
            self.wait(random.randint(1, 5))
            self.wait(70)
            return best_ball
        return None

    def __check_weight_ball(self, weight):
        if weight > 204.8:
            if self.check_ball_in_inventary("heavy_ball"):
                best_ball = "heavyball"
                self.wait()
                return best_ball

        if weight <= 9.9:
            if self.check_ball_in_inventary("feather_ball"):
                best_ball = "featherball"
                self.wait()
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
                    self.wait()
                    return best_ball

        return None

    def __check_event_ball(self, types):
        if not self.event:
            return None
        for type in types:
            if type == "Bug":
                return "sport_ball"
        return None

    def __check_stats_ball(self, stats):
        if stats["vit"] > 100:
            if self.check_ball_in_inventary("fast_ball"):
                best_ball = "fastball"
                self.wait()
                return best_ball

        if stats["hp"] > 100:
            if self.check_ball_in_inventary("heal_ball"):
                best_ball = "healball"
                self.wait()
                return best_ball

        return None

    def __check_ultra_ball(self):
        if self.check_ball_in_inventary("ultra_ball"):
            best_ball = "ultraball"
            self.wait()
            return best_ball
        return None

    def __check_low_ball(self):
        # 55%
        if self.check_ball_in_inventary("great_ball"):
            best_ball = "greatball"
            self.wait()
            return best_ball

        if self.check_ball_in_inventary("luxury_ball"):
            best_ball = "luxuryball"
            self.wait()
            return best_ball

        # 40%
        if self.check_ball_in_inventary("level_ball"):
            best_ball = "levelball"
            self.wait()
            return best_ball

        # 30%
        if self.check_ball_in_inventary("clone_ball"):
            best_ball = "cloneball"
            self.wait()
            return best_ball

        if self.check_ball_in_inventary("poke_ball"):
            best_ball = " "
            self.wait()
            return best_ball

        if self.check_ball_in_inventary("premier_ball"):
            best_ball = " "
            self.wait()
            return best_ball
        return None

    def wait(self, time: int = 0):
        if not time:
            time = random.randint(5, 80)

        asyncio.run(self.__wait_coroutine(time))

    async def __wait_coroutine(self, time: int):
        await asyncio.sleep(time)
        return True
