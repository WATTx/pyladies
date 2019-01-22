#!/bin/sh

ESP_PORT=${1:-/dev/tty.SLAB_USBtoUART}

export AMPY_PORT=$ESP_PORT

wget http://micropython.org/resources/firmware/esp8266-20180511-v1.9.4.bin

esptool.py --port $ESP_PORT erase_flash

esptool.py --port $ESP_PORT \
    --baud 115200 write_flash -fm dio -fs 4MB -ff 40m 0x00000 \
    esp8266-20180511-v1.9.4.bin