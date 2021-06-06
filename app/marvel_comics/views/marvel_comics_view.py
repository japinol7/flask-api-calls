import hashlib
import logging
import os
from pathlib import Path
import requests
from datetime import datetime
from flask import render_template, request
from app import app

from ..models.marvel_comic import MarvelComic
from ..models.marvel_general_data import MarvelGeneralData
from ...utils import utils


MARVEL_COMICS_WEBSITE = "https://www.marvel.com/comics/"
MARVEL_API_KEY_FOLDER = os.path.join(str(Path.home()), 'marvel_api_keys')
MARVEL_API_KEY_FILE = os.path.join(MARVEL_API_KEY_FOLDER, 'marvel_public_key.key')
MARVEL_API_PRIVATE_KEY_FILE = os.path.join(MARVEL_API_KEY_FOLDER, 'marvel_private_key.key')

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.route('/marvel-comics', methods=['GET', 'POST'])
def marvel_comic():
    comics = []
    form_executed = None
    if request.method == 'POST' and 'marvel_comics_title' in request.form:
        title = request.form.get('marvel_comics_title')
        limit = request.form.get('marvel_comics_limit')
        offset = request.form.get('marvel_comics_offset')
        start_date = request.form.get('marvel_comics_start_date')
        end_date = request.form.get('marvel_comics_end_date') or start_date
        title_match_method = request.form.get('marvel_comics_title_method')
        order_by = request.form.get('marvel_comics_order_by')
        comics = get_marvel_comics(title, limit, offset, start_date, end_date, title_match_method, order_by)
        form_executed = 'marvel_form_comics'
    return render_template('marvel_comics.html', comics=comics, form_executed=form_executed)


def get_marvel_comics(title, limit, offset, start_date, end_date, title_match_method, order_by):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    api_key = utils.read_file_as_string(MARVEL_API_KEY_FILE)
    private_key = utils.read_file_as_string(MARVEL_API_PRIVATE_KEY_FILE)
    raw_hash = ts + private_key + api_key
    md5_hash = hashlib.md5(raw_hash.encode()).hexdigest()
    offset_txt = f"&offset={offset}" if offset else ''
    date_range = f"{start_date},{end_date}" if start_date and end_date else ''
    date_range_txt = f"&dateRange={date_range}" if date_range else ''
    title_match_method_search = 'title' if title_match_method == 'exact_match' else 'titleStartsWith'
    r = requests.get(f"https://gateway.marvel.com:443/v1/public/comics?"
                     f"format=comic&formatType=comic&"
                     f"limit={limit}{offset_txt}{date_range_txt}&"
                     f"noVariants=True&"
                     f"{title_match_method_search}={title}&"
                     f"ts={ts}&apikey={api_key}&hash={md5_hash}&"
                     f"orderBy={order_by}")
    if not r.ok:
        error_msg = get_marvel_request_msg_error(a_request=r)
        res = ((title, limit, offset, start_date, end_date, title_match_method, order_by),
               0, None, [], {'error': error_msg})
        logger.info(res)
        return res

    comics = []
    comics_data = r.json()
    marvel_gen_data = MarvelGeneralData(code=comics_data['code'])
    fill_marvel_general_data_fields(marvel_gen_data, comics_data)
    for item in comics_data['data']['results']:
        comic = MarvelComic(id=item['id'],
                            name=item['title'])
        fill_comic_fields(comic, item)
        comics.append(comic)
    return ((title, limit, offset, start_date, end_date, title_match_method, order_by),
            len(comics), marvel_gen_data, comics, {'error': ''})


def fill_comic_fields(comic, item):
    comic.digital_id = item.get('digitalId')
    comic.issue_number = item.get('issueNumber')
    comic.variant_description = item.get('variantDescription')
    comic.description = item.get('description')
    comic.urls = item.get('urls')
    comic.url = comic.urls and comic.urls[0].get('url') or ''
    comic.resource_URI = item.get('resourceURI')
    comic.creators = item.get('creators')
    comic.characters = item.get('characters')
    comic.page_count = item.get('pageCount')
    comic.ean = item.get('ean')
    comic.isbn = item.get('isbn')
    comic.variant_description = item.get('variantDescription')

    thumbnail = item.get('thumbnail')
    if thumbnail:
        comic.thumbnail = f"{thumbnail.get('path')}.{thumbnail.get('extension')}"

    urls = item.get('urls') and item.get('urls')
    comic.urls = []
    if urls:
        for url in urls:
            comic.urls.append(url.get('url'))
    else:
        comic.urls.append(MARVEL_COMICS_WEBSITE)

    images = item.get('images') and item.get('images')
    comic.images = []
    if images:
        for image in images:
            comic.images.append(f"{image.get('path')}.{image.get('extension')}")

    creators = item.get('creators') and item.get('creators').get('items')
    comic.creators = []
    if creators:
        for creator in creators:
            comic.creators.append({'name': creator['name'], 'role': creator['role']})

    characters = item.get('characters') and item.get('characters').get('items')
    comic.characters = []
    if characters:
        for character in characters:
            comic.characters.append(character['name'])

    series = item.get('series') and item.get('series').get('items')
    comic.series = []
    if series:
        for series_one in series:
            comic.series.append(series_one['name'])

    stories = item.get('stories') and item.get('stories').get('items')
    comic.stories = []
    if stories:
        for story in stories:
            comic.stories.append(f"{story['name']}: {story['type']}")

    events = item.get('events') and item.get('events').get('items')
    comic.events = []
    if events:
        for event in events:
            comic.events.append(event['name'])


def fill_marvel_general_data_fields(obj, data_pulled):
    obj.status = data_pulled.get('status')
    obj.copyright = data_pulled.get('copyright')
    obj.attribution_text = data_pulled.get('attributionText')
    obj.attribution_HTML = data_pulled.get('attributionHTML')
    obj.etag = data_pulled.get('etag')
    obj.total_matches = data_pulled['data']['total']


def get_marvel_request_msg_error(a_request):
    r = a_request
    error_msg = ''
    if r.ok:
        return error_msg

    if r.content:
        r_json = r.json()
        error_msg = f"{r_json.get('code')}. {r_json.get('message')}"
    return error_msg
