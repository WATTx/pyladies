import machine
import ubinascii
from time import sleep
from lib import bme280
from lib.umqtt import MQTTClient

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
bme = bme280.BME280(i2c=i2c)

do_connect()

# MQTT server to connect to
HOST = "your_machine_host"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"data"

client = MQTTClient(CLIENT_ID, HOST)
client.connect()

print("Connected to %s" % HOST)

while(True):
    temperature, pressure, humidity = bme.values
    print("Temperature: {}º C\nPressure: {} hPa\nHumidity {}%\n".format(
        temperature, pressure, humidity))
    client.publish(TOPIC, temperature)

    sleep(3)
