import sys

from pokemon import Pokemon

if __name__ == "__main__":

    id = None

    args = sys.argv

    for arg in args:
        if arg.startswith("id="):
            id = int(arg[3:])

    if not id:
        print("Please provide an id")
        sys.exit()

    pokemon = Pokemon(id=id)

    print(f"Pokemon {pokemon.en_name} fetched")
