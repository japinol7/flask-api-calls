from ...tools.logger.logger import log
import requests
from flask import render_template, request
from app import app

from ..models.nasa_asteroid import Asteroid


@app.route('/nasa-asteroid', methods=['GET', 'POST'])
def nasa():
    asteroids = []
    form_executed = None
    if request.method == 'POST' and 'nasa_asteroids_start_date' in request.form:
        start_date = request.form.get('nasa_asteroids_start_date')
        end_date = request.form.get('nasa_asteroids_end_date') or start_date
        asteroids = get_nasa_asteroids(start_date, end_date)
        form_executed = 'nasa_form_approach_date'
    elif request.method == 'POST' and 'nasa_asteroids_neo_ref_id' in request.form:
        asteroid_id = request.form.get('nasa_asteroids_neo_ref_id')
        asteroids = get_nasa_asteroids_by_id(asteroid_id)
        form_executed = 'nasa_form_neo_ref_id'
    return render_template('nasa_asteroid.html', asteroids=asteroids, form_executed=form_executed)


def get_nasa_asteroids(start_date, end_date):
    r = requests.get(f"https://api.nasa.gov/neo/rest/v1/feed?"
                     f"start_date={start_date}&end_date={end_date}&api_key=DEMO_KEY")
    if not r.ok:
        error_msg = get_nasa_request_msg_error(a_request=r)
        res = (start_date, end_date), 0, [], {'error': error_msg}
        log.info(res)
        return res

    asteroids = []
    asteroids_data = r.json()
    for approach_date in asteroids_data['near_earth_objects']:
        for item in asteroids_data['near_earth_objects'][approach_date]:
            asteroid = Asteroid(id=item['id'],
                                neo_reference_id=item['neo_reference_id'],
                                name=item['name'])
            asteroid.close_approach_date = approach_date
            fill_asteroid_fields(asteroid, item)
            asteroids.append(asteroid)
    return (start_date, end_date), len(asteroids), asteroids, {'error': ''}


def get_nasa_asteroids_by_id(asteroid_id):
    r = requests.get(f"https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key=DEMO_KEY")
    if not r.ok:
        error_msg = get_nasa_request_msg_error(a_request=r)
        res = (asteroid_id, asteroid_id), 0, [], {'error': error_msg}
        log.info(res)
        return res

    asteroids = []
    item = r.json()
    asteroid = Asteroid(id=item['id'],
                        neo_reference_id=item['neo_reference_id'],
                        name=item['name'])
    asteroid.close_approach_date = item['close_approach_data'][0]['close_approach_date']
    fill_asteroid_fields(asteroid, item)
    asteroids.append(asteroid)
    return (asteroid_id, asteroid_id), len(asteroids), asteroids, {'error': ''}


def fill_asteroid_fields(asteroid, item):
    asteroid.nasa_jpl_url = item['nasa_jpl_url']
    asteroid.absolute_magnitude_h = item['absolute_magnitude_h']
    asteroid.estimated_diameter_km_min = item['estimated_diameter']['kilometers']['estimated_diameter_min']
    asteroid.estimated_diameter_km_max = item['estimated_diameter']['kilometers']['estimated_diameter_max']
    asteroid.is_potentially_hazardous_asteroid = item['is_potentially_hazardous_asteroid']
    if len(item['close_approach_data']) > 1:
        log.info(f"Asteroid {asteroid.id}. There are several asteroid 'close_approach_data' items."
                    f"But we will take only the first one. We should consider to take all this data.")
    close_approach_data = item['close_approach_data'][0]
    asteroid.relative_velocity_km_per_sec = close_approach_data['relative_velocity']['kilometers_per_second']
    asteroid.relative_velocity_km_per_hour = close_approach_data['relative_velocity']['kilometers_per_hour']
    asteroid.miss_distance_km = close_approach_data['miss_distance']['kilometers']
    asteroid.miss_distance_astronomical = close_approach_data['miss_distance']['astronomical']
    asteroid.orbiting_body = close_approach_data['orbiting_body']
    asteroid.is_sentry_object = item['is_sentry_object']


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
