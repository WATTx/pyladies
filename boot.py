# Wemos board pin mapping
import esp
import network
esp.osdebug(None)

D0 = 16
D1 = 5
D2 = 4
D3 = 0
D4 = 2
D5 = 14
D6 = 12
D7 = 13
D8 = 15
RX = 3
TX = 1
BUILTIN_LED = 2


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        SSID = 'ssid'
        wifi_key = 'key'
        print('Connecting to ' + SSID)
        sta_if.active(True)
        sta_if.connect(SSID, wifi_key)
        while not sta_if.isconnected():
            pass
    print('Network config:', sta_if.ifconfig())
