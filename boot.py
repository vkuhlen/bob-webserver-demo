import network
import config

_WLAN_SSID = ''
_WLAN_PASSWORD = ''
_WLAN_ENCRYPTION = network.WLAN.WPA2

wlan = network.WLAN(mode=network.WLAN.STA)
wlan.connect(
    _WLAN_SSID,
    auth=(_WLAN_ENCRYPTION, _WLAN_PASSWORD)
)