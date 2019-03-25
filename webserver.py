import machine
import time
import binascii

from microWebSrv import MicroWebSrv

import sensors
from config import Config

_config = Config()

# To not run into trouble with CORS while developing
_headers = {'Access-Control-Allow-Origin': '*'}

@MicroWebSrv.route('/restart')
def restart(httpClient, httpResponse):
    machine.reset()


##############################################################################
# Routes for sensor readings #################################################
##############################################################################

@MicroWebSrv.route('/api/sensors/<sensor>')
def measure_ds1820(httpClient, httpResponse, routeArgs):
    sensor = routeArgs['sensor']
    if hasattr(sensors, sensor):

        # Read sensor DS1820
        if sensor == 'ds1820':
            ds = sensors.ds1820
            for rom in ds.roms:
                ds.start_conversion(rom=rom)
            time.sleep_ms(750)
            data = {}
            for rom in ds.roms:
                data[binascii.hexlify(rom).decode('utf-8')] = ds.read_temp_async(rom=rom)

        # Read sensor HX711
        elif sensor == 'hx711':
            hx = sensors.hx711
            data = {'weight': hx.read_average(times=5)}

        # Read sensor BME280
        elif sensor == 'bme280':
            bme = sensors.bme280
            data = {}
            (data['t'],
            data['p'],
            data['h']) = bme.read_compensated_data()

        return httpResponse.WriteResponseJSONOk(obj=data, headers=_headers)
    else:
        return httpResponse.WriteResponseJSONError(404)


##############################################################################
# Routes for working with the config #########################################
##############################################################################

@MicroWebSrv.route('/api/config')
def get_config(httpClient, httpResponse):
    return httpResponse.WriteResponseJSONOk(obj=_config.data, headers=_headers)

@MicroWebSrv.route('/api/config/<section>/<subsection>', 'GET')
def get_config_subsection(httpClient, httpResponse, routeArgs):
    section = routeArgs['section']
    subsection = routeArgs['subsection']

    data = _config.data.get(section, {}).get(subsection, None)
    if data is None:
        return httpResponse.WriteResponseJSONError(404)
    else:
        return httpResponse.WriteResponseJSONOk(
            obj=data,
            headers=_headers)

@MicroWebSrv.route('/api/config/<section>/<subsection>', 'POST')
def post_config_subsection(httpClient, httpResponse, routeArgs):
    section = routeArgs['section']
    subsection = routeArgs['subsection']
    form_data = httpClient.ReadRequestContentAsJSON()

    if not section in _config.data.keys():
        _config.data[section] = {}

    _config.data[section][subsection] = form_data
    _config.write()
    return httpResponse.WriteResponseJSONOk(
        obj={'status': 'saved'},
        headers=_headers)

@MicroWebSrv.route('/api/config/<section>/<subsection>', 'DELETE')
def delete_config_subsection(httpClient, httpResponse, routeArgs):
    section = routeArgs['section']
    subsection = routeArgs['subsection']

    if section in _config.data.keys():
        data = _config.data[section].pop(subsection, None)
    
    if data is None:
        return httpResponse.WriteResponseJSONError(404)
    else:
        _config.write()
        return httpResponse.WriteResponseJSONOk(
            obj={'status': 'deleted'},
            headers=_headers)

@MicroWebSrv.route('/api/config/<section>/<subsection>', 'OPTIONS')
def options_config(httpClient, httpResponse, routeArgs):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'}
    return httpResponse.WriteResponseOk(
        headers = headers,
        contentType = "text/plain",
        contentCharset = "UTF-8",
        content="")

mws = MicroWebSrv()