from pokemonDB import TypeDB
import requests

from unidecode import unidecode

if __name__ == "__main__":

    api_url = "https://tyradex.vercel.app/api/v1/types"
    db = TypeDB()

    res = requests.get(api_url)

    for type in res.json():

        t = {
            "id": type["id"],
            "name_fr": unidecode(type["name"]["fr"]),
            "name_en": type["name"]["en"],
        }
        db.save_type(t)
