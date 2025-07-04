import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import func
import json


class PokemonDB:
    def __init__(self):
        self.engine = sqlalchemy.create_engine("sqlite:///pokemon.db")
        self.connection = self.engine.connect()
        self.metadata = sqlalchemy.MetaData()

        # Define the table schema
        self.pokemon = sqlalchemy.Table(
            "pokemon",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("pokemon_id", Integer),
            Column("generation", Integer),
            Column("name_fr", String),
            Column("name_en", String),
            Column("types", String),
            Column("stats", String),
            Column("height", Integer),
            Column("weight", Integer),
            Column("region", String, nullable=True),
        )

        # Create the table if it doesn't exist
        self.metadata.create_all(self.engine)

    def save_pokemon(self, pokemon):
        query = sqlalchemy.insert(self.pokemon).values(
            pokemon_id=pokemon["pokemon_id"],
            region=pokemon["region"],
            generation=pokemon["generation"],
            name_fr=pokemon["name_fr"],
            name_en=pokemon["name_en"],
            types=json.dumps(pokemon["types"]),  # Convert to JSON string
            stats=json.dumps(pokemon["stats"]),  # Convert to JSON string
            height=pokemon["height"],
            weight=pokemon["weight"],
        )
        self.connection.execute(query)
        self.connection.commit()

    def get_pokemon(self, name, lang, region=None):
        if lang == "fr":
            name_column = self.pokemon.c.name_fr
        elif lang == "en":
            name_column = self.pokemon.c.name_en
        else:
            return None

        conditions = [func.lower(name_column) == func.lower(name)]
        if region is not None:
            conditions.append(func.lower(self.pokemon.c.region)
                              == func.lower(region))
        else:
            conditions.append(self.pokemon.c.region.is_(None))
        query = sqlalchemy.select(self.pokemon).where(*conditions)

        result = self.connection.execute(query).fetchone()
        if result:
            result_dict = dict(result._mapping)
            result_dict["types"] = json.loads(
                result_dict["types"]
            )  # Convert back to dictionary
            result_dict["stats"] = json.loads(
                result_dict["stats"]
            )  # Convert back to dictionary
            return result_dict
        return None

    def get_all_pokemon(self):
        query = sqlalchemy.select(self.pokemon)
        result = self.connection.execute(query).fetchall()
        return [dict(row._mapping) for row in result]

    def get_pokemon_id(self, id, region=None):
        conditions = [self.pokemon.c.pokemon_id == id]
        if region is not None:
            conditions.append(func.lower(self.pokemon.c.region)
                              == func.lower(region))
        else:
            conditions.append(self.pokemon.c.region.is_(None))
        query = sqlalchemy.select(self.pokemon).where(*conditions)
        result = self.connection.execute(query).fetchone()
        if result:
            result_dict = dict(result._mapping)
            result_dict["types"] = json.loads(
                result_dict["types"]
            )  # Convert back to dictionary
            result_dict["stats"] = json.loads(
                result_dict["stats"]
            )  # Convert back to dictionary
            return result_dict
        return None


class TypeDB:
    def __init__(self):
        self.engine = sqlalchemy.create_engine("sqlite:///pokemon.db")
        self.connection = self.engine.connect()
        self.metadata = sqlalchemy.MetaData()

        # Define the table schema
        self.types = sqlalchemy.Table(
            "types",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name_fr", String),
            Column("name_en", String),
        )

        # Create the table if it doesn't exist
        self.metadata.create_all(self.engine)

    def save_type(self, type):
        query = sqlalchemy.insert(self.types).values(
            id=type["id"],
            name_fr=type["name_fr"],
            name_en=type["name_en"],
        )
        self.connection.execute(query)
        self.connection.commit()

    def get_type(self, name):
        query = sqlalchemy.select(self.types).where(
            func.lower(self.types.c.name_fr) == func.lower(name)
        )
        result = self.connection.execute(query).fetchone()
        if result:
            result_dict = dict(result._mapping)
            return result_dict
        return None
