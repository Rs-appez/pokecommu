from models.pokemon import Pokemon

import re


class PokemonDataMapper:
    regions = {
        "alo": "alola",
        "gal": "galar",
        "his": "hisui",
        "sin": "sinnoh",
    }

    @classmethod
    def get_pokemon_from_chat(cls, pokemon_name : str, lang : str) -> Pokemon | None:
        def get_reg_form(p):
            name_split = p.split(" ")
            for form in cls.regions.keys():
                if name_split[0] == form:
                    return form

        def get_spe_form(p):
            form = re.search(r"\(.*?\)", p)
            if form:
                return form.group(0)[1:-1]

        pokemon = pokemon_name.lower()

        if reg_form := get_reg_form(pokemon):
            pokemon = pokemon.replace(reg_form, "", 1)

        region = cls.regions.get(reg_form, None)

        if spe_form := get_spe_form(pokemon):
            pokemon = pokemon.replace(f"({spe_form})", "", 1)

        pcg = pokemon.startswith("pcg")

        pokemon = pokemon.strip()

        match lang:
            case "fr":
                return Pokemon(name_fr=pokemon, reg_form=region)
            case "en":
                return Pokemon(
                    name_en=pokemon, reg_form=region, spe_form=spe_form, pcg=pcg
                )
            case _:
                raise ValueError(f"Language {lang} not supported")

    @classmethod
    def get_pokemon_from_pcg(cls, pokemon_data: dict) -> Pokemon | None:
        def get_reg_form(p) -> str | None:
            name_split = p.split("-")

            for form in cls.regions.values():
                if name_split[-1] == form:
                    return f"-{form}"
                if name_split[0] == form:
                    return f"{form}-"

        pokemon: Pokemon = None
        name: str = pokemon_data.get("name", "")
        id: int = pokemon_data.get("order", 0)

        if not name or id == 0:
            return None

        if reg_form := get_reg_form(name):
            name = name.replace(reg_form, "")
            reg_form = reg_form.replace("-", "")

        pokemon = Pokemon(id=id, reg_form=reg_form)
        name = name.replace(pokemon.en_name.lower(), "")

        pokemon.spe_form = name.replace("-", " ").strip() or None

        return pokemon


if __name__ == "__main__":
    print("Testing PokemonData module:")
    pikachu = PokemonDataMapper.get_pokemon_from_chat("pikachu", "en")
    vulpix_alo = PokemonDataMapper.get_pokemon_from_chat("alo vulpix", "en")
    vulpix_alo_pcg = PokemonDataMapper.get_pokemon_from_pcg(
        {
            "name": "vulpix-alola",
            "order": 37,
        }
    )
    avalugg_his = PokemonDataMapper.get_pokemon_from_pcg(
        {
            "name": "hisuian-avalugg",
            "order": 713,
        }
    )
    basculin = PokemonDataMapper.get_pokemon_from_pcg(
        {
            "name": "basculin-blue-striped",
            "order": 550,
        }
    )
    arcanine = PokemonDataMapper.get_pokemon_from_pcg(
        {
            "name": "arcanine-pcg",
            "order": 59,
        }
    )

    ratata = PokemonDataMapper.get_pokemon_from_pcg(
        {
            "name": "rattata-alola",
            "order": 19,
        }
    )

    print(pikachu)
    print(vulpix_alo)
    print(vulpix_alo_pcg)
    print(avalugg_his)
    print(basculin)
    print(arcanine)
    print(ratata)
