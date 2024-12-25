from pokemonDB import PokemonDB

class Pokemon():
    
    db = PokemonDB()

    def __init__(self, name = None, id = 0):

        self.fr_name = name
        self.id = id

        self.fr_types = []
        self.en_types = []
        self.en_name = None
        self.stats = []
        self.height = 0
        self.weight = 0 
