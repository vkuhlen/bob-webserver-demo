import network
import binascii

from config import Config

_WLAN_SSID = 'hiverize'
_WLAN_PASSWORD = ''
_WLAN_ENCRYPTION = network.WLAN.WPA2

wlan = network.WLAN(mode=network.WLAN.STA)

# Initial WLan scan to get a list of visible SSIDs
config = Config()
ssids = [ {
    'ssid': s.ssid,
    'bssid': binascii.hexlify(s.bssid).decode('utf-8'),
    'sec': s.sec,
    'channel': s.channel} for s in wlan.scan() ]
config.data['networking']['wlan']['available'] = ssids
config.write()

wlan.connect(
    _WLAN_SSID,
    auth=(_WLAN_ENCRYPTION, _WLAN_PASSWORD)
)