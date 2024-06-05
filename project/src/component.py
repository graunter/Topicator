import paho.mqtt.client as mqtt
import math

class CComponent:
    def __init__(self, InTopicName: str, OutTopicName: str, Operation: str=""):
        self.InTopicName = InTopicName
        self.OutTopicName = OutTopicName
        self.Expr = Operation
        
        self.InPayload: str
        self.OutPayload: str

        #self.Code = compile(self.Expr, "<string>", "eval")

    def on_connect(self, client: mqtt.Client):
        client.subscribe( self.InTopicName )  

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        
        if not self.Expr:
            client.publish( self.OutTopicName, msg.payload)
        else:
            self.InPayload = msg.payload
            Tmp = eval( self.Expr, {}, {"In": int(self.InPayload), "Out": self.OutPayload})
            self.OutPayload = Tmp

            client.publish( self.OutTopicName, self.OutPayload)