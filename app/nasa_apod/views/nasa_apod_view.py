from ...tools.logger.logger import log
import requests
from flask import render_template, request
from app import app

from ..models.nasa_apod import NasaApod


@app.route('/nasa-apod', methods=['GET', 'POST'])
def nasa_apod():
    apods = []
    form_executed = None
    if request.method == 'POST' and 'nasa_apod_start_date' in request.form:
        start_date = request.form.get('nasa_apod_start_date')
        end_date = request.form.get('nasa_apod_end_date') or start_date
        apods = get_nasa_apods(start_date, end_date)
        form_executed = 'nasa_form_apod_date'
    elif request.method == 'POST' and 'nasa_apod_random_total' in request.form:
        apods_qty = request.form.get('nasa_apod_random_total')
        apods = get_nasa_apods_random(qty=apods_qty)
        form_executed = 'nasa_form_apod_random'
    return render_template('nasa_apod.html', apods=apods, form_executed=form_executed)


def get_nasa_apods(start_date, end_date):
    r = requests.get(f"https://api.nasa.gov/planetary/apod?"
                     f"start_date={start_date}&end_date={end_date}&api_key=DEMO_KEY")
    if not r.ok:
        error_msg = get_nasa_request_msg_error(a_request=r)
        res = (start_date, end_date), 0, [], {'error': error_msg}
        log.info(res)
        return res

    apods = []
    apods_data = r.json()
    id = 0
    for item in apods_data:
        id += 1
        apod = NasaApod(id=id,
                        name=item['title'])
        fill_apod_fields(apod, item)
        apods.append(apod)
    return (start_date, end_date), len(apods), apods, {'error': ''}


def get_nasa_apods_random(qty):
    r = requests.get(f"https://api.nasa.gov/planetary/apod?"
                     f"count={qty}&api_key=DEMO_KEY")
    if not r.ok:
        error_msg = get_nasa_request_msg_error(a_request=r)
        res = (qty, qty), 0, [], {'error': error_msg}
        log.info(res)
        return res

    apods = []
    apods_data = r.json()
    id = 0
    for item in apods_data:
        id += 1
        apod = NasaApod(id=id,
                        name=item['title'])
        fill_apod_fields(apod, item)
        apods.append(apod)
    return (qty, qty), len(apods), apods, {'error': ''}


def fill_apod_fields(apod, item):
    apod.date = item.get('date')
    apod.title = item.get('title')
    apod.explanation = item.get('explanation')
    apod.url = item.get('url')
    apod.url_hd = item.get('hdurl')
    apod.media_type = item.get('media_type')
    apod.copyright = item.get('copyright')
    apod.service_version = item.get('service_version')


def get_nasa_request_msg_error(a_request):
    r = a_request
    error_msg = ''
    if r.ok:
        return error_msg

    if r.content:
        r_json = r.json()
        if 'error_message' in r_json.keys():
            error_msg = r_json['error_message']
        elif 'error' in r_json.keys():
            error_msg = r_json['error'].get('message', '')
    return error_msg
