import requests
from flask import render_template, request
from app import app


@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    pokemon = []
    if request.method == 'POST' and 'pokemon_color' in request.form:
        color = request.form.get('pokemon_color')
        pokemon = get_pokemon_of_color(color)
    return render_template('pokemon.html', pokemon=pokemon)


def get_pokemon_of_color(color):
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon-color/{color.lower()}")
    if not r.ok:
        return color, 0, []

    pokemon = []
    pokedata = r.json()
    for item in pokedata['pokemon_species']:
        pokemon.append((item['name'], item['url']))

    return color, len(pokemon), pokemon
