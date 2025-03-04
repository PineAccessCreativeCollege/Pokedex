import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json


def SearchPokemon(search_term):
    url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"


    response = requests.get(url, timeout=50)
    pokemon_data_global = response.json()
    #print(pokemon_data_global)

    percentage_result = []
    for pokemon in pokemon_data_global['results']:
        ratio = fuzz.ratio(search_term, pokemon['name'])
        percentage_result.append(ratio)
        #print(f"{pokemon['name']} - {ratio}%")

    best_matches = []
    for i in range(10):
        print(f"Best match: {pokemon_data_global['results'][percentage_result.index(max(percentage_result))]['name']}")
        best_matches.append(pokemon_data_global['results'][percentage_result.index(max(percentage_result))]['name'])
        percentage_result.remove(max(percentage_result))

    print(best_matches)
    return best_matches

if __name__ == "__main__":
    SearchPokemon()