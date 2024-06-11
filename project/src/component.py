#from __future__ import division    # this option could be used for division test

import paho.mqtt.client as mqtt
import math
#from math import sin, cos, tan, asin, acos, atan, log, log10, exp, ceil, floor
from math import *
import logging
import decimal
import ast

#from fastnumbers import isfloat, isint #pip3 install fastnumbers

def isint(arg) -> bool:
    test_num = int.from_bytes(arg, byteorder='big', signed=True)
    if arg == test_num.to_bytes(test_num, byteorder='big', signed=True):
        return True
    else:
        return False
    

def isfloat(arg) -> bool:
    if b"." in arg:
        return True
    else:
        return False

class CComponent:
    def __init__(self, InTopicName: str, OutTopicName: str, Operation: str=""):
        self.InTopicName = InTopicName
        self.OutTopicName = OutTopicName
        self.Expr = Operation
        
        self.InPayload: str
        self.OutPayload = 0

        #self.Code = compile(self.Expr, "<string>", "eval")

    def on_connect(self, client: mqtt.Client):
        client.subscribe( self.InTopicName )  
        logging.debug('Subscription: ' + self.InTopicName + ' -> ' + self.Expr + ' -> ' + self.OutTopicName)

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        
        self.InPayload = msg.payload
        
        available_functions = {
            'pi': math.pi,
            'e': math.e,
            'sin': sin,
            'cos': cos,
            'tan': tan, 
            'asin': asin, 
            'acos': acos, 
            'atan': atan, 
            'log': log, 
            'log10': log10, 
            'exp': exp, 
            'ceil': ceil, 
            'floor': floor
        }

        if not self.Expr:
            self.OutPayload = self.InPayload
        else:
            try:
                if isfloat((msg.payload)):
                    number = float(msg.payload)
                #elif isint((msg.payload)):
                #    number = int(float(msg.payload))
                else:
                    number = int(msg.payload)
                #else:
                #    logging.error('Cant recognise this type in argument In: ' + str(self.InPayload) + ' - set to zero')
                #    number = 0
        
            #try:
                self.OutPayload = eval( self.Expr,  available_functions, {"In": number})
                
            except (TypeError)  as e:
                logging.error('Type err in this expression: ' + self.Expr + ' with argument In: ' + str(self.InPayload) + ': Message: ' + format(e) )
                pass
            except NameError as e:
                logging.error('Name err in expression: ' + self.Expr + ' with argument In: ' + str(self.InPayload) + ': Message: ' + format(e) )
                pass
            except SyntaxError as e:
                logging.error('Syntax err in expression: ' + self.Expr + ': Message: ' + format(e) )
                pass
            except ZeroDivisionError as e: 
                logging.error('Division by Zero: ' + self.Expr + ' with argument In: ' + str(self.InPayload) + ' is fail')
                pass
            except ValueError as e:
                logging.error("Can't use this expression: " + self.Expr + ' with this Input: ' + str(self.InPayload) + ': Message: ' + format(e) )
                pass
            except Exception as e:
                logging.error("Unknown err in this expression: " + self.Expr + ' with this Input: ' + str(self.InPayload) + ': Message: ' + format(e) )
                pass                


        client.publish( self.OutTopicName, self.OutPayload)