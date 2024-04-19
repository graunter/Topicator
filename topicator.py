#!/usr/bin/env python3

import os, re, time, json, argparse, signal
import paho.mqtt.client as mqtt # pip install paho-mqtt
import urllib.parse

verbose = False

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    client.disconnect()


parser = argparse.ArgumentParser(description='Send MQTT payload received from a topic to any.', 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-a', '--adr-broker', dest='host', action="store", default="127.0.0.1",
                   help='Specify the MQTT host to connect to.')
parser.add_argument('-p', '--port-broker', dest='port', action="store", default="1883",
                   help='Specify the MQTT host to connect to.')
parser.add_argument('-i', '--in_topic', dest='itopic', action="store", default="Test/In/#",
                   help='The listening MQTT topic.')
parser.add_argument('-o', '--out_topic', dest='otopic', action="store", default="Test/Out",
                   help='The output MQTT topic.')
parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", default=False,
                   help='Enable debug messages.')


def debug(msg):
    if verbose:
        print (msg + "\n")

def on_connect(client, userdata, flags, rc):
    debug("Connected with result code "+str(rc))
    # Подписка при подключении означает, что если было потеряно соединение
    # и произошло переподключение - то подписка будет обновлена
    client.subscribe(args.itopic)

def on_message(client, userdata, msg):
    InTopicName = msg.topic.split('/') [-1]

    tstamp = int(time.time())
    mqttPath = urllib.parse.urljoin(args.otopic + '/', InTopicName)
    debug("Received message from {0} with payload {1} to be published to {2}".format(msg.topic, str(msg.payload), mqttPath))
    nodeData = msg.payload
    client.publish(mqttPath, nodeData)




if __name__ == "main":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    args = parser.parse_args()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(args.host, int(args.port), 60)

    client.loop_forever()