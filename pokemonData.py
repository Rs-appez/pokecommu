from pokemon import Pokemon


class PokemonData:

    regional_forms = ["alo", "gal", "his", "sin"]

    def get_pokemon(self, pokemon, lang) -> Pokemon | None:

        pokemon_object = None

        if lang == "num":
            pokemon = int(pokemon)

        if type(pokemon) is str:

            pokemon = pokemon.lower()
            form = self.__get_form(pokemon)
            if form:
                pokemon = pokemon.replace(form, "", 1).strip()

            if lang == "fr":
                pokemon_object = Pokemon(name_fr=pokemon, form=form)
            elif lang == "en":
                pokemon_object = Pokemon(name_en=pokemon, form=form)

        elif type(pokemon) is int:
            pokemon_object = Pokemon(id=pokemon)

        return pokemon_object

    def __get_form(self, pokemon):
        for form in self.regional_forms:
            if pokemon.startswith(form):
                return form
