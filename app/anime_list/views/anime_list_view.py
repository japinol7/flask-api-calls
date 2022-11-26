import requests
from flask import render_template, request
from app import app


@app.route('/anime-list', methods=['GET', 'POST'])
def anime_list():
    anime_list = []
    if request.method == 'POST' and 'anime_list_title' in request.form:
        title = request.form.get('anime_list_title')
        anime_list = get_anime_list_of_title(title)
    return render_template('anime_list.html', anime_list=anime_list)


def get_anime_list_of_title(title):
    r = requests.get(f"https://api.jikan.moe/v4/anime/?q={title.lower()}&page=1")
    if not r.ok:
        return title, 0, []

    anime_list = []
    anime_data = r.json()
    for item in anime_data['data']:
        anime_list.append((item['mal_id'], item['title'], item['url'], item['images']['jpg']['image_url']))

    return title, len(anime_list), anime_list
