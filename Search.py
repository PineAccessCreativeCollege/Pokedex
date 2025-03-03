import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json

url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"


def InitPokemon():
    response = requests.get(url, timeout=50)
    pokemon_data_global = response.json()
    print(pokemon_data_global)
    return pokemon_data_global
    
def PokemonSlots():
    i = 0
    for i in range(5):
        pass
        ##Do this later cus idk
    

pokemon_data_global = InitPokemon()
with open('pokemon_data_globaljson.json', 'w') as f:
    json.dump(pokemon_data_global, f)

##PokemonSlots