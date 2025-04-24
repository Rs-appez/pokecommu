from pokemon import Pokemon

import re


class PokemonData:
    regional_forms = ["alo", "gal", "his", "sin"]

    def get_pokemon(self, pokemon, lang) -> Pokemon | None:
        pokemon_object = None

        if lang == "num":
            pokemon = int(pokemon)

        if type(pokemon) is str:
            pokemon = pokemon.lower()

            reg_form = self.__get_reg_form(pokemon)
            if reg_form:
                pokemon = pokemon.replace(reg_form, "", 1).strip()

            spe_form = self.__get_spe_form(pokemon)
            print("spe_form : ", spe_form)

            if spe_form:
                pokemon = pokemon.replace(f"({spe_form})", "", 1).strip()

            if lang == "fr":
                pokemon_object = Pokemon(name_fr=pokemon, reg_form=reg_form)
            elif lang == "en":
                pokemon_object = Pokemon(
                    name_en=pokemon, reg_form=reg_form, spe_form=spe_form
                )

        elif type(pokemon) is int:
            pokemon_object = Pokemon(id=pokemon)

        return pokemon_object

    def __get_reg_form(self, pokemon):
        for form in self.regional_forms:
            if pokemon.startswith(form):
                return form

    def __get_spe_form(self, pokemon):
        form = re.search(r"\(.*?\)", pokemon)
        if form:
            return form.group(0)[1:-1]
