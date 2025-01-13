from pokemon import Pokemon


class PokemonData:

    def get_pokemon(self, pokemon, lang):

        if type(pokemon) is str:

            if lang == "fr":
                pokemon = Pokemon(name_fr=pokemon)
            elif lang == "en":
                pokemon = Pokemon(name_en=pokemon)

        elif type(pokemon) is int:
            pokemon = Pokemon(id=pokemon)

        else:
            pokemon = None

        return pokemon
