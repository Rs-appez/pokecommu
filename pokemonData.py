from pokemon import Pokemon


class PokemonData:

    def get_pokemon(self, pokemon, lang) -> Pokemon | None:

        pokemon_object = None

        if lang == "num":
            pokemon = int(pokemon)

        if type(pokemon) is str:

            if lang == "fr":
                pokemon_object = Pokemon(name_fr=pokemon)
            elif lang == "en":
                pokemon_object = Pokemon(name_en=pokemon)

        elif type(pokemon) is int:
            pokemon_object = Pokemon(id=pokemon)

        return pokemon_object
