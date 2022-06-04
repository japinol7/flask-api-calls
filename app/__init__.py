from flask import Flask

app = Flask(__name__)

from . import views
from . import pokemon
from . import anime_list
from . import nasa_apod
from . import nasa_asteroid
from . import nasa_exoplanet
from . import marvel_comics
from . import spotify_music
from . import dog_breeds
