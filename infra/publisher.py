import argparse
import sys
import logging
from logging import INFO
import json
from time import sleep

from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt

logging.basicConfig(level=INFO)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        userdata['connected'] = True
        logging.info("Successfully connected to the MQTT broker at " +
                     client._host + ". Code " + str(rc))
    else:
        logging.info("Bad connection. Code " + str(rc))


def parse_args():
    parser = argparse.ArgumentParser(
        description='Triggers an MQTT message when a new part is ready to be classified')
    parser.add_argument("--hostname", default="localhost",
                        help="MQTT broker hostname")
    parser.add_argument("--qos", default=1,
                        help="QoS level", choices=[0, 1, 2])
    parser.add_argument("--topic", default="data",
                        help="Topic root, typically the same as ClientId")
    parser.add_argument("--clientname", default="part_publisher",
                        help="Client Id, used for persistent sessions")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    hostname = args.hostname
    qos = args.qos
    topic = args.topic
    client_name = args.clientname

    influx_client = InfluxDBClient(host='localhost', port=8086)

    userdata = {'connected': False,
                'influx_client': influx_client}

    mqtt_client = mqtt.Client(client_id=client_name, userdata=userdata)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(hostname)
    sleep(1)
    mqtt_client.loop_start()
    mqtt_client.subscribe(topic, qos=qos)

    while not userdata['connected']:
        logging.info("Waiting for connection to broker...")
        sleep(3)

    while True:
        try:
            sleep(0.1)
            pass
        except KeyboardInterrupt:
            logging.info("\nDisconnecting from " + hostname)
            mqtt_client.disconnect()
            mqtt_client.loop_stop()
            sleep(1)
            logging.info("Done")
            sys.exit()


def on_message(client, userdata, message):
    msg = json.loads(message.payload)

    logging.info("Message payload" + str(msg))
    influx_client = userdata['influx_client']

    logging.info("temp:" + msg.temperature)
    json_body = [
        {
            "measurement": "temperature",
            "fields": {
                "value": msg['temperature']
            }
        }
    ]
    print(influx_client.write_points(json_body))


if __name__ == "__main__":
    main()
