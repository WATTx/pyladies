import machine
from lib import bme280
from time import sleep

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
bme = bme280.BME280(i2c=i2c)

i = 0
while(i < 10):
    temperature, pressure, humidity = bme.values
    print("Temperature: {}º C\nPressure: {} hPa\nHumidity {}%\n".format(
        temperature, pressure, humidity))
    sleep(3)
    i = i + 1
