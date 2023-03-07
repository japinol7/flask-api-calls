import os
from pathlib import Path

SPEAK_TIMEOUT = 7
OPENAI_API_KEY_FOLDER = os.path.join(str(Path.home()), '.api_keys', 'openai_api_keys')
OPENAI_API_KEY_FILE = os.path.join(OPENAI_API_KEY_FOLDER, 'openai_private_key.key')
LANGUAGE = 'en'
AUDIO_FILE_EXT = '.mp3'
