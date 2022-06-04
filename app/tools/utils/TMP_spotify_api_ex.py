import os
from pathlib import Path
from app.tools.utils import utils
from app.tools.logger.logger import logger as log

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_API_KEY_FOLDER = os.path.join(str(Path.home()), '.api_keys', 'spotify_api_keys')
SPOTIFY_API_KEY_FILE = os.path.join(SPOTIFY_API_KEY_FOLDER, 'spotify_client_id.key')
SPOTIFY_API_PRIVATE_KEY_FILE = os.path.join(SPOTIFY_API_KEY_FOLDER, 'spotify_client_secret.key')


def main():
    os.environ['SPOTIPY_CLIENT_ID'] = utils.read_file_as_string(SPOTIFY_API_KEY_FILE)
    os.environ['SPOTIPY_CLIENT_SECRET'] = utils.read_file_as_string(SPOTIFY_API_PRIVATE_KEY_FILE)

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    artist_name = 'Hilary Hahn'
    results = spotify.search(q=f'artist:{artist_name}', type='artist')
    items = results['artists']['items']
    if len(items) < 1:
        log.warning(f"Artist not found:{artist_name}")
        return

    if len(items) > 1:
        log.warning(f"Found {len(items)} artists that match the artist name: '{artist_name}'. "
                    f"We choose the first and discard the rest.")

    artist = items[0]
    artist_uri = artist['uri']
    artist_url = artist['external_urls']['spotify']
    log.info(f"Artist: {artist['name']}, {artist_url}")

    results = spotify.artist_albums(artist_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        log.info(f"Album: {album['name']}")


if __name__ == '__main__':
    main()
