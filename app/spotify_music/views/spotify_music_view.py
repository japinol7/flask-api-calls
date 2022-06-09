import logging

from flask import render_template, request

from app import app
from app.spotify_music.controller.spotify_music_controller import SpotifyMusicController

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.route('/spotify-music', methods=['GET', 'POST'])
def spotify_music():
    sp_music_data = []
    form_executed = None
    if request.method == 'POST' and 'spotify_music_artist_uri_id' in request.form:
        artist = request.form.get('spotify_music_artist')
        album = request.form.get('spotify_music_album')
        artist_uri_id = request.form.get('spotify_music_artist_uri_id')
        artist_match_method = request.form.get('spotify_artist_match_method')
        limit = int(request.form.get('spotify_albums_limit'))
        start_date = request.form.get('spotify_albums_start_date')
        end_date = request.form.get('spotify_albums_end_date') or start_date
        order_by = request.form.get('spotify_albums_order_by')
        form_executed = 'spotify_form_albums'

        music_controller = SpotifyMusicController(artist, limit, start_date, end_date, artist_match_method,
                                                  artist_uri_id, order_by, only_artists=False, album_name=album)
        sp_music_data = music_controller.get_spotify_music()
    elif request.method == 'POST' and 'spotify_artist_uri_id' in request.form:
        artist = request.form.get('spotify_artist')
        limit = int(request.form.get('spotify_artist_limit'))
        artist_uri_id = request.form.get('spotify_artist_uri_id')
        form_executed = 'spotify_form_artists'

        music_controller = SpotifyMusicController(artist, limit, None, None, None, artist_uri_id, None,
                                                  only_artists=True, album_name=None)
        sp_music_data = music_controller.get_spotify_music()
    return render_template('spotify_music.html', sp_music_data=sp_music_data, form_executed=form_executed)
