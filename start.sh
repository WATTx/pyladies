#!/bin/sh -e

ESP_PORT=${1:-/dev/tty.SLAB_USBtoUART}
FIRMWARE_VERSION=${2:-esp8266-20180511-v1.9.4.bin}

export ESP_PORT
export AMPY_PORT=$ESP_PORT

curl http://micropython.org/resources/firmware/$FIRMWARE_VERSION --output $FIRMWARE_VERSION

esptool.py --port $ESP_PORT erase_flash

esptool.py --port $ESP_PORT \
    --baud 115200 write_flash -fm dio -fs 4MB -ff 40m 0x00000 \
    $FIRMWARE_VERSION