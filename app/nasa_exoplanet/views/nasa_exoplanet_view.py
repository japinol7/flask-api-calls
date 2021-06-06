import logging
import requests
from flask import render_template, request
from app import app

from ..models.nasa_exoplanet import Exoplanet

EXOPLANET_COLUMNS = [
    'pl_name',
    'pl_letter',
    'pl_hostname',
    'pl_discmethod',
    'pl_controvflag',
    'pl_pnum',
    'pl_orbper',
    'pl_orbsmax',
    'pl_orbeccen',
    'pl_orbincl',
    'pl_bmassj',
    'pl_bmassprov',
    'pl_radj',
    'pl_dens',
    'dec',
    'rowupdate',
    'pl_facility',
    'st_teff',
    'st_mass',
    'st_rad',
    ]

logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.route('/nasa-exoplanet', methods=['GET', 'POST'])
def nasa_exoplanet():
    exoplanets = []
    form_executed = None
    if request.method == 'POST' and 'exoplanet_option' in request.form:
        option = request.form.get('exoplanet_option')
        exoplanets = get_nasa_exoplanets(option)
        form_executed = 'nasa_form_exoplanets'
    return render_template('nasa_exoplanet.html', exoplanets=exoplanets, form_executed=form_executed)


def get_nasa_exoplanets(option):
    columns_to_get = ','.join(EXOPLANET_COLUMNS)
    r = requests.get(f"https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI"
                     f"?table=exoplanets&select={columns_to_get}&order=pl_name&format=json")
    if not r.ok:
        error_msg = get_nasa_request_msg_error(a_request=r)
        res = (option, option), 0, [], {'error': error_msg}
        logger.info(res)
        return res

    exoplanets = []
    exoplanets_data = r.json()
    id = 0
    for item in exoplanets_data:
        id += 1
        apod = Exoplanet(id=id,
                         name=item.get('pl_name'))
        fill_exoplanet_fields(apod, item)
        exoplanets.append(apod)
    return (option, option), len(exoplanets), exoplanets, {'error': ''}


def fill_exoplanet_fields(exoplanet, item):
    exoplanet.pl_name = item.get('pl_name')
    exoplanet.pl_letter = item.get('pl_letter')
    exoplanet.pl_hostname = item.get('pl_hostname')
    exoplanet.pl_discmethod = item.get('pl_discmethod')
    exoplanet.pl_controvflag = item.get('pl_controvflag')
    exoplanet.pl_pnum = item.get('pl_pnum')
    exoplanet.pl_orbper = item.get('pl_orbper')
    exoplanet.pl_orbsmax = item.get('pl_orbsmax')
    exoplanet.pl_orbeccen = item.get('pl_orbeccen')
    exoplanet.pl_orbincl = item.get('pl_orbincl')
    exoplanet.pl_bmassj = item.get('pl_bmassj')
    exoplanet.pl_bmassprov = item.get('pl_bmassprov')
    exoplanet.pl_radj = item.get('pl_radj')
    exoplanet.pl_dens = item.get('pl_dens')
    exoplanet.dec = item.get('dec')
    exoplanet.rowupdate = item.get('rowupdate')
    exoplanet.pl_facility = item.get('pl_facility')
    exoplanet.st_teff = item.get('st_teff')
    exoplanet.st_mass = item.get('st_mass')
    exoplanet.st_rad = item.get('st_rad')


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
