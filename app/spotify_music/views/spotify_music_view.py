import logging
import os
from pathlib import Path
from flask import render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app import app
from app.tools.logger.logger import logger as log
from ..models.spotify_album import SpotifyAlbum
from ..models.spotify_artist import SpotifyArtist
from ...tools.utils import utils

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

MIN_ARTIST_FOLLOWERS = 2
MIN_ARTIST_POPULARITY = 1

SPOTIFY_API_KEY_FOLDER = os.path.join(str(Path.home()), '.api_keys', 'spotify_api_keys')
SPOTIFY_API_KEY_FILE = os.path.join(SPOTIFY_API_KEY_FOLDER, 'spotify_client_id.key')
SPOTIFY_API_PRIVATE_KEY_FILE = os.path.join(SPOTIFY_API_KEY_FOLDER, 'spotify_client_secret.key')
os.environ['SPOTIPY_CLIENT_ID'] = utils.read_file_as_string(SPOTIFY_API_KEY_FILE)
os.environ['SPOTIPY_CLIENT_SECRET'] = utils.read_file_as_string(SPOTIFY_API_PRIVATE_KEY_FILE)


@app.route('/spotify-music', methods=['GET', 'POST'])
def spotify_music():
    albums = []
    form_executed = None
    if request.method == 'POST' and 'spotify_music_artist_uri' in request.form:
        artist = request.form.get('spotify_music_artist')
        artist_match_method = request.form.get('spotify_artist_match_method')
        limit = int(request.form.get('spotify_albums_limit'))
        start_date = request.form.get('spotify_albums_start_date')
        end_date = request.form.get('spotify_albums_end_date') or start_date
        order_by = request.form.get('spotify_albums_order_by')
        albums = get_spotify_music(artist, limit, start_date, end_date, artist_match_method, order_by)
        form_executed = 'spotify_form_albums'
    elif request.method == 'POST' and 'spotify_artist_uri' in request.form:
        form_executed = 'spotify_form_artists'
    return render_template('spotify_music.html', albums=albums, form_executed=form_executed)


def get_spotify_music(artist_name, limit, start_date, end_date, artist_match_method, order_by,
                      only_artists=False, only_one_artist=True):
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    SpotifyArtist.reset_num_id()
    SpotifyAlbum.reset_num_id()

    artist_results = spotify.search(q=f'artist:{artist_name}', type='artist')
    artist_items = artist_results['artists']['items']
    if len(artist_items) < 1:
        error_msg = "Artist not found"
        res = ((artist_name, limit, start_date, end_date, artist_match_method, order_by),
               0, None, [], {'error': error_msg})
        log.info(res)
        return res

    if len(artist_items) > 1:
        log.warning(f"Found {len(artist_items)} artists that match the artist name: '{artist_name}'. "
                    f"We choose the first and discard the rest.")

    artist_data = artist_items[0]
    artist = SpotifyArtist(artist_data['id'])
    fill_artist_fields(artist, artist_data)
    log.info(f"Artist: {artist.name}, followers: {artist.followers} "
             f"popularity: {artist.popularity} uri/url {artist.uri} {artist.url}")

    albums = []
    if not only_artists:
        get_spotify_albums(spotify, artist, limit)
        albums = SpotifyAlbum.albums

    if not only_one_artist:
        get_spotify_other_artists(artist_items, artist_data)

    return ((artist_name, limit, start_date, end_date, artist_match_method, order_by),
            len(albums), SpotifyArtist.artists, albums, {'error': ''})


def get_spotify_albums(spotify, artist, limit):
    albums = []
    albums_results = spotify.artist_albums(artist.uri, album_type='album')
    albums_data = albums_results['items']
    while albums_results['next'] and len(albums_data) < limit:
        albums_results = spotify.next(albums_results)
        albums_data.extend(albums_results['items'])

    for album_data in albums_data[:limit]:
        log.info(f"Album: {album_data['name']}")
        album = SpotifyAlbum(id=album_data['id'])
        fill_album_fields(album, album_data, artist)
        albums.append(album)


def get_spotify_other_artists(artist_items, artist_data):
    log.info(f"{'-' * 15}")
    for other_artist_data in artist_items[1:]:
        followers = other_artist_data['followers']['total']
        popularity = other_artist_data['popularity']
        if followers < MIN_ARTIST_FOLLOWERS and popularity < MIN_ARTIST_POPULARITY:
            continue
        other_artist = SpotifyArtist(artist_data['id'])
        fill_artist_fields(other_artist, other_artist_data)
        log.info(f"--- Another artist: {other_artist.name}, followers: {other_artist.followers} "
                 f"popularity: {other_artist.popularity} uri/url {other_artist.uri} {other_artist.url}")


def fill_album_fields(album, item, artist):
    album.name = item['name']
    album.artist = artist
    album.artists = [x['name'] for x in item['artists']]
    album.uri = item['uri']
    album.url = item['external_urls']['spotify']
    album.image_url = item['images'] and item['images'][0]['url'] or None
    album.release_date = item['release_date']
    album.total_tracks = item['total_tracks']
    album.album_type = item['album_type']
    album.type = item['type']


def fill_artist_fields(artist, item):
    artist.name = item['name']
    artist.followers = item['followers']['total']
    artist.uri = item['uri']
    artist.url = item['external_urls']['spotify']
    artist.image_url = item['images'] and item['images'][0]['url'] or None
    artist.popularity = item['popularity']
