import paho.mqtt.client as mqtt

class CComponent:
    def __init__(self, InTopicName, OutTopicName):
        self.InTopicName = InTopicName
        self.OutTopicName = OutTopicName

    def on_connect(self, client: mqtt.Client):
        client.subscribe( self.InTopicName )  

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        client.publish( self.OutTopicName, msg.payload)