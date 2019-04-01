# FiPy demo server implementation for the BOB project

This is a small demo implementation of a webserver running on the FiPy.

It is intended as a reference backend implementation for a JavaScript based frontend.

## Setup

### WiFi settings

For easy use I recommend to set up the WLan on the FiPy to be reachable from your PC. All headers are set to communicate with the API without running into problems with [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).

To setup the WLan open `boot.py` and set

```python
    _WLAN_SSID = ''
    _WLAN_PASSWORD = ''
    _WLAN_ENCRYPTION = network.WLAN.WPA2
```

If you need additional options please refer to the [PyCom documentation](https://docs.pycom.io/firmwareapi/pycom/network/wlan.html).

> **The WLan settings are only set in `boot.py`!** The WLan configuration in the JSON file is supposed to be the primary configuration but it'd be annoying to lose the connection while testing.

### Installation

Install the pymakr plugin for Atom/VSCode as [described here](https://docs.pycom.io/pymakr/installation/).
Afterwards open this folder in your editor and click upload in the pymakr command bar.

If you want to reset your FiPy connect to the REPL and run
```python
import os
os.mkfs('/flash')
```

### How to find the FiPys IP

#### FiPy REPL

If you have access to the REPL you can find the IP with
```python
import network
w = network.WLAN(id=0)
w.ifconfig()[0]
```

#### Using `nmap` (Linux only)

First open a console window.
Find your PCs IP address with
```
ip addr | grep 'inet '
```

Then type
```
nmap -sn [YOUR IP ADDRESS]/24
```
This will display all devices in your LAN. If one device is called `espressif` it is your FiPy. If there is no such device listed you have to try all IP addresses.

## Configuration via JSON

The API is based around a single JSON file where the settings for your program are stored.
The JSON file is structured with sections and subsections e.g.:

```json
{
    "networking": {
        "wlan": {
            "ssid": "Foo",
            "password": "Bar"
        }
    }
}
```

This block could then be read with a `GET` request to `http://[your_fipy_ip]/api/config/networking/wlan`.

### Implemented methods

Each url `http://[your_fipy_ip]/api/config/[section]/[subsection]` implements the methods `GET`, `POST`, `DELETE` and `OPTIONS`.

#### `GET`

As described above the server responds with the JSON block from the file `settings.json`. If section or subsection are not found it returns a empty JSON object with status `404`.

#### `POST`

You can write JSON to a section/subsection with an `POST` request. This overwrites an existing block so make sure you include all keys you need.
On success the server returns a JSON object `{"status": "saved"}`.
Try it with
```bash
curl -d '{"this": "is", "test": "data"}' http://[your_fipy_ip]]/api/config/test/testdata
curl http://[your_fipy_ip]]/api/config/test/testdata
```

** In the future a `PUT` method should be implemented to edit/update a section without overwriting the whole block. **

#### `DELETE`

A `DELETE` request deletes the whole block from the JSON file. On success it returns a JSON object `{"status": "deleted"}`. If the section/subsection is not found it returns an empty JSON objkect with status code `404`.
Try it with:
```bash
curl -X DELETE http://[your_fipy_ip]]/api/config/test/testdata
```
Now try deleting it again and display the response header:
```bash
curl -I -X DELETE http://[your_fipy_ip]]/api/config/test/testdata
```

#### `OPTIONS`

The options method is needed for the [CORS preflight request](https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request)

## Implemented sensors

Currently three sensors are implemented:

- DS1820: Temperature
- HX711: Weight
- BME280: Temperature, Pressure, Humidity (over I2C)

The pins used are set in the file `settings.json'.

### Routes

A sensor can be read with a `GET` request to e.g. `http://[your_fipy_ip]]/api/sensors/ds1820`.