import os
from pathlib import Path

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.tools.logger.logger import logger as log
from ..models.spotify_album import SpotifyAlbum
from ..models.spotify_artist import SpotifyArtist
from ...tools.utils import utils

MIN_ARTIST_FOLLOWERS = 2
MIN_ARTIST_POPULARITY = 1
ARTISTS_LIMIT_MARGIN_DISCARDED = 25

SPOTIFY_API_KEY_FOLDER = os.path.join(str(Path.home()), '.api_keys', 'spotify_api_keys')
SPOTIFY_API_KEY_FILE = os.path.join(SPOTIFY_API_KEY_FOLDER, 'spotify_client_id.key')
SPOTIFY_API_PRIVATE_KEY_FILE = os.path.join(SPOTIFY_API_KEY_FOLDER, 'spotify_client_secret.key')
os.environ['SPOTIPY_CLIENT_ID'] = utils.read_file_as_string(SPOTIFY_API_KEY_FILE)
os.environ['SPOTIPY_CLIENT_SECRET'] = utils.read_file_as_string(SPOTIFY_API_PRIVATE_KEY_FILE)


class SpotifyMusicController:

    def __init__(self, artist_name, limit, start_date, end_date, artist_match_method,
                 artist_uri_id, order_by, only_artists=False, album_name=None):
        self.artist_name = artist_name
        self.limit = limit
        self.start_date = start_date
        self.end_date = end_date
        self.artist_match_method = artist_match_method
        self.artist_uri_id = artist_uri_id
        self.order_by = order_by
        self.only_artists = only_artists
        self.album_name = album_name

        self.spotify = None
        self.albums = None
        self.artists = None

        self.reset()

    def reset(self):
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        SpotifyArtist.reset()
        SpotifyAlbum.reset()

    def get_spotify_music(self):
        artist_items = []
        album_results = {}

        if not self.artist_name and not self.artist_uri_id and not self.album_name:
            error_msg = "Not enough input data."
            res = ((self.artist_name, self.limit, self.start_date, self.end_date,
                    self.artist_match_method, self.artist_uri_id, self.order_by, self.album_name),
                   0, None, [], {'error': error_msg})
            log.info(res)
            return res

        try:
            if self.artist_uri_id:
                artist_data = self.spotify.artist(self.artist_uri_id)
                artist_results = {'artists': {
                    'items': [artist_data],
                    'next': None,
                }}
                artist_items = artist_results['artists']['items']
            elif not self.album_name:
                query = f'artist:{self.artist_name}'
                artist_results = self.spotify.search(q=query, type='artist')
                artist_items = artist_results['artists']['items']
            else:
                query = f'album:{self.album_name}, artist:{self.artist_name}' if self.artist_name else f'album:{self.album_name}'
                album_results = self.spotify.search(q=query, type='album')
                album_results = album_results['albums']
        except spotipy.SpotifyException as e:
            log.warning(f"SpotifyException: {e}")

        if not self.album_name and len(artist_items) < 1:
            error_msg = "No artist found" if self.only_artists else "Artist not found"
            res = ((self.artist_name, self.limit, self.start_date, self.end_date, self.artist_match_method,
                    self.artist_uri_id, self.order_by, self.album_name),
                   0, None, [], {'error': error_msg})
            log.info(res)
            return res

        if not self.album_name and len(artist_items) > 1:
            log.warning(f"Found {len(artist_items)} artists that match the artist name: '{self.artist_name}'. "
                        f"We choose the first and discard the rest.")

        if not self.album_name:
            artist_data = artist_items[0]
            artist = SpotifyArtist(artist_data['id'])
            self.fill_artist_fields(artist, artist_data)
            log.info(f"Artist: {artist.name}, followers: {artist.followers} "
                     f"popularity: {artist.popularity} uri/url {artist.uri} {artist.url}")

        albums = []
        if self.album_name:
            self.get_spotify_albums(album_results)
            albums = SpotifyAlbum.albums
            items_len = len(albums)
        elif self.only_artists:
            self.get_spotify_other_artists(artist_results)
            items_len = len(SpotifyArtist.artists)
        else:
            self.get_spotify_albums_from_artist(artist)
            albums = SpotifyAlbum.albums
            items_len = len(albums)

        return ((self.artist_name, self.limit, self.start_date, self.end_date, self.artist_match_method,
                 self.artist_uri_id, self.order_by, self.album_name),
                items_len, SpotifyArtist.artists, albums, {'error': ''})

    def get_spotify_albums(self, albums_results):
        albums = []
        albums_data = albums_results['items']
        while albums_results['next'] and len(albums_data) < self.limit:
            albums_results = self.spotify.next(albums_results)['albums']
            albums_data.extend(albums_results['items'])

        for album_data in albums_data[:self.limit]:
            log.info(f"Album: {album_data['name']}")
            album = SpotifyAlbum(id=album_data['id'])
            artist_data = album_data['artists'][0]
            artist = SpotifyArtist(artist_data['id'])
            artist.name = artist_data['name']
            artist.uri = artist_data['uri']
            artist.url = artist_data['external_urls']['spotify']
            self.fill_album_fields(album, album_data, artist)
            albums.append(album)

    def get_spotify_albums_from_artist(self, artist):
        albums = []
        albums_results = self.spotify.artist_albums(artist.uri, album_type='album')
        albums_data = albums_results['items']
        while albums_results['next'] and len(albums_data) < self.limit:
            albums_results = self.spotify.next(albums_results)
            albums_data.extend(albums_results['items'])

        for album_data in albums_data[:self.limit]:
            log.info(f"Album: {album_data['name']}")
            album = SpotifyAlbum(id=album_data['id'])
            self.fill_album_fields(album, album_data, artist)
            albums.append(album)

    def get_spotify_other_artists(self, artist_results):
        artists_data = artist_results['artists']['items']
        limit_effective = self.limit + ARTISTS_LIMIT_MARGIN_DISCARDED
        while artist_results['artists']['next'] and len(artists_data) < limit_effective:
            artist_results = self.spotify.next(artist_results['artists'])
            artists_data.extend(artist_results['artists']['items'])

        log.info(f"{'-' * 15}")
        for other_artist_data in artists_data[1:]:
            followers = other_artist_data['followers']['total']
            popularity = other_artist_data['popularity']
            if followers < MIN_ARTIST_FOLLOWERS and popularity < MIN_ARTIST_POPULARITY:
                continue
            if len(SpotifyArtist.artists) >= self.limit:
                break
            other_artist = SpotifyArtist(other_artist_data['id'])
            self.fill_artist_fields(other_artist, other_artist_data)
            log.info(f"--- Another artist: {other_artist.name}, followers: {other_artist.followers} "
                     f"popularity: {other_artist.popularity} uri/url {other_artist.uri} {other_artist.url}")

    def fill_album_fields(self, album, item, artist):
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

    def fill_artist_fields(self, artist, item):
        artist.name = item['name']
        artist.followers = item['followers']['total']
        artist.uri = item['uri']
        artist.url = item['external_urls']['spotify']
        artist.image_url = item['images'] and item['images'][0]['url'] or None
        artist.popularity = item['popularity']
