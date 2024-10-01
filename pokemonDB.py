import sqlalchemy
from sqlalchemy import Column, Integer, String
import json

class PokemonDB:
    def __init__(self):
        self.engine = sqlalchemy.create_engine('sqlite:///pokemon.db')
        self.connection = self.engine.connect()
        self.metadata = sqlalchemy.MetaData()

        # Define the table schema
        self.pokemon = sqlalchemy.Table('pokemon', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('type', String),
            Column('stats', String),
            Column('height', Integer),
            Column('weight', Integer)
        )

        # Create the table if it doesn't exist
        self.metadata.create_all(self.engine)

    def save_pokemon(self, pokemon):
        query = sqlalchemy.insert(self.pokemon).values(
            id=pokemon['id'],
            name=pokemon['name'],
            type=json.dumps(pokemon['type']),  # Convert to JSON string
            stats=json.dumps(pokemon['stats']),  # Convert to JSON string
            height=pokemon['height'],
            weight=pokemon['weight']
        )
        self.connection.execute(query)
        self.connection.commit()

    def get_pokemon(self, name):
        query = sqlalchemy.select(self.pokemon).where(self.pokemon.c.name == name)
        result = self.connection.execute(query).fetchone()
        if result:
            result_dict = dict(result._mapping)
            result_dict['type'] = json.loads(result_dict['type'])  # Convert back to dictionary
            result_dict['stats'] = json.loads(result_dict['stats'])  # Convert back to dictionary
            return result_dict
        return None
