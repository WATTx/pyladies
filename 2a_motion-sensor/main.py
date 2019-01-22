from machine import Pin
import micropython
from time import sleep

micropython.alloc_emergency_exception_buf(100)
led = Pin(D5, Pin.OUT)

do_connect()


def motion_callback(v):
    print("Motion detected")
    led.off()
    for i in range(0, 4):
        led.value(not led.value())
        sleep(0.5)


motion_sensor = Pin(D7, Pin.IN)
motion_sensor.irq(trigger=Pin.IRQ_RISING, handler=motion_callback)

while(True):
    sleep(1)
    pass
