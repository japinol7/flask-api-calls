from ...tools.logger.logger import log
import requests
from flask import render_template, request
from app import app

from ..models.nasa_exoplanet import Exoplanet

EXOPLANET_COLUMNS = [
    'pl_name',
    'pl_letter',
    'hostname',
    'discoverymethod',
    'pl_controv_flag',
    'sy_pnum',
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
    'disc_facility',
    'st_teff',
    'st_mass',
    'st_radv',
    ]


@app.route('/nasa-exoplanet', methods=['GET', 'POST'])
def nasa_exoplanet():
    exoplanets = []
    form_executed = None
    if request.method == 'POST' and 'exoplanet_option' in request.form:
        option = request.form.get('exoplanet_option')
        name = request.form.get('exoplanet_name')
        exoplanets = get_nasa_exoplanets(option, name)
        form_executed = 'nasa_form_exoplanets'
    return render_template('nasa_exoplanet.html', exoplanets=exoplanets, form_executed=form_executed)


def get_nasa_exoplanets(option, name):
    columns_to_get = ','.join(EXOPLANET_COLUMNS)
    name_sql_filter = f"+where+upper(pl_name)+like+'%{name.upper()}%'" if name else ''
    r = requests.get(f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="
                     f"select+{columns_to_get}+from+ps{name_sql_filter}+order+by+pl_name+&format=json")
    if not r.ok:
        error_msg = get_nasa_request_msg_error(a_request=r)
        res = (option, option), 0, [], {'error': error_msg}
        log.info(res)
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
    exoplanet.pl_hostname = item.get('hostname')
    exoplanet.pl_discmethod = item.get('discoverymethod')
    exoplanet.pl_controvflag = item.get('pl_controv_flag')
    exoplanet.pl_pnum = item.get('sy_pnum')
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
    exoplanet.pl_facility = item.get('disc_facility')
    exoplanet.st_teff = item.get('st_teff')
    exoplanet.st_mass = item.get('st_mass')
    exoplanet.st_rad = item.get('st_radv')


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
