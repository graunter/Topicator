#!/usr/bin/env python3

import os, re, time, json, argparse, signal
import paho.mqtt.client as mqtt # pip install paho-mqtt
import urllib.parse
from config import MyConfig

class Topicator:
    def __init__(self, Cfg):
        self.verbose = False
        self.cfg = Cfg

    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        client.disconnect()

    def debug(self, msg):
        if self.verbose:
            print (msg + "\n")

    def on_connect(self, client, userdata, flags, rc):
        
        self.debug("Connected with result code "+str(rc))
        # Подписка при подключении означает, что если было потеряно соединение
        # и произошло переподключение - то подписка будет обновлена
        for Topic in Cfg.topics.keys():
            client.subscribe(Topic)   

    def on_message(self, client, userdata, msg):
        #InTopicName = msg.topic.split('/') [-1]
        tstamp = int(time.time())
        #mqttPath = urllib.parse.urljoin(args.otopic + '/', InTopicName)
        mqttPath = msg.topic

        OutTopic = Cfg.topics.get(msg.topic)
        if OutTopic is not None:
            self.debug("Received message from {0} with payload {1} to be published to {2}".format(msg.topic, str(msg.payload), mqttPath))    
        
            nodeData = msg.payload
            client.publish(OutTopic, nodeData)




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Send MQTT payload received from a topic to any.', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    
    parser.add_argument('-a', '--adr-broker', dest='host', action="store",
                    help='Specify the MQTT host to connect to.')
    parser.add_argument('-p', '--port-broker', dest='port', action="store",
                    help='Specify the MQTT host to connect to.')    
    parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", default=False,
                    help='Enable debug messages.')

    
    Cfg = MyConfig()
    
    topicator = Topicator(Cfg)

    signal.signal(signal.SIGINT, topicator.signal_handler)
    signal.signal(signal.SIGTERM, topicator.signal_handler)

    topicator.debug("Topicator started!")

    client = mqtt.Client()
    client.on_connect = topicator.on_connect
    client.on_message = topicator.on_message

    args = parser.parse_args()
    
    Host = args.host if args.host is not None else Cfg.host
    Port = args.port if args.host is not None else Cfg.port

    client.connect(Host, Port)
        
    client.loop_forever()

