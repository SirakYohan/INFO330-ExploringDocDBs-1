from pymongo import MongoClient
import sqlite3

# 1. import all of your packages (missing sqlite3)
# 2. set up sqlite connection (copy what you did for HW6
# 3. for loop over the number of pokemon in the DB (SELECT COUNT(*)...
# 4. get all the info for each pokemon needed to populate the json (according to the example) -- this may take multiple queries
# Note: run your files using python filename.py -- make sure that you're in the project repo for this
mongoClient = MongoClient("mongodb://localhost/pokemon")
pokemonDB = mongoClient['pokemondb']
pokemonColl = pokemonDB['pokemon_data']


conn = sqlite3.connect("/Users/sirak/Documents/INFO-330/INFO330-ExploringDocDBs/pokemon.sqlite")
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM pokemon')
num_pokemon = cursor.fetchone()[0]
for i in range(1, num_pokemon + 1):
    X = cursor.execute('SELECT pokemon.name, pokemon.pokedex_number, pokemon.hp, pokemon.defense, pokemon.sp_attack, pokemon.sp_defense, ability.name FROM pokemon join ability on ability.id == pokemon.id WHERE pokedex_number=?', (i,))
    pokemon = X.fetchone()
    j = cursor.execute('SELECT type.name FROM type \
                   JOIN pokemon_type ON type.id = pokemon_type.type_id \
                   WHERE pokemon_type.pokemon_id = ?', (i,))
    types = ', '.join([t[0] for t in j.fetchall()])

    I = cursor.execute('SELECT ability.name FROM ability JOIN pokemon ON pokemon.id = ability.id \
                       WHERE ability.id = ?', (i,))
    abilities = ', '.join([a[0] for a in I.fetchall()])

    ##still getting none type error even when I fetchnone, did extra credit in battle.py
    document = {
        "name": pokemon[0],
        "pokedex_number": pokemon[1],
        "types": types,
        "hp": pokemon[2],
        "defense": pokemon[3],
        "sp_attack": pokemon[4],
        "sp_defense": pokemon[5],
        "abilities": abilities,
    }

    pokemonColl.insert_one(document)

    ## querys
    pikachu = pokemonColl.find_one({"name": "Pikachu"})
    strong_pokemon = pokemonColl.find({"attack": {"$gt": 150}})
    overgrow_pokemon = pokemonColl.find({"ability": "Overgrow"})

    print(document)
