#!/usr/bin/env python3

import os, re, time, json, argparse, signal
import paho.mqtt.client as mqtt # pip install paho-mqtt
from my_config import MyConfig
import paho.mqtt.client as mqtt
import logging


class CTopicator:
    def __init__(self, Cfg: MyConfig):
        self.verbose = False
        self.cfg = Cfg
        self.componets = Cfg.get_components()


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

        for i, (key, CompLst) in enumerate(self.componets.items()):
            for OneComp in CompLst:
                OneComp.on_connect( client )


    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):

        #if msg.topic in self.componets:
        for item in self.componets[msg.topic]:
            item.on_message( client, userdata, msg)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Send MQTT payload received from a topic to any.', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    
    parser.add_argument('-a', '--adr-broker', dest='host', action="store",
                    help='Specify the MQTT host to connect to.')
    parser.add_argument('-p', '--port-broker', dest='port', action="store",
                    help='Specify the MQTT host to connect to.')    
    parser.add_argument('-v', '--verbose', dest='verbose', action="store_true", default=False,
                    help='Enable debug messages.')

    args = parser.parse_args()
    
    loglevel = logging.INFO 
    if args.verbose: 
        loglevel = logging.DEBUG

    logging.basicConfig(level=loglevel)
    
    Cfg = MyConfig()
    
    topicator = CTopicator(Cfg)
    if args.verbose: 
        topicator.verbose = True


    signal.signal(signal.SIGINT, topicator.signal_handler)
    signal.signal(signal.SIGTERM, topicator.signal_handler)

    topicator.debug("Topicator started!")

    client = mqtt.Client()
    client.on_connect = topicator.on_connect
    client.on_message = topicator.on_message
    
    Host = args.host if args.host is not None else Cfg.host
    Port = args.port if args.host is not None else Cfg.port

    client.connect(Host, Port)
        
    client.loop_forever()

