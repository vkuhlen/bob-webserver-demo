from machine import Pin, I2C
import time

import onewire

from config import Config
import sensors.ds18x20
import sensors.bme280
import sensors.hx711

_config = Config()

if 'sensors' in _config.data.keys():

    _ds_config = _config.data['sensors'].get('ds1820', {})
    if _ds_config.get('enabled', False):
        ow = onewire.OneWire(
            Pin(_ds_config['pin']))
        time.sleep_ms(100)
        ds1820 = sensors.ds18x20.DS18X20(ow)

    _hx_config =  _config.data['sensors'].get('hx711', {})
    if _hx_config.get('enabled', False):
        hx711 = sensors.hx711.HX711(
            _hx_config['pin_dout'],
            _hx_config['pin_pdsck']
        )

    _bme_config = _config.data['sensors'].get('bme280', {})
    if _bme_config.get('enabled'), False):
        i2c = I2C(0, I2C.MASTER, pins=(
            _bme_config['pin_sda'],
            _bme_config['pin_scl']
        ))
        bme280 = sensors.bme280.BME280(address=0x77, i2c=i2c)