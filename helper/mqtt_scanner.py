#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import paho.mqtt.client as mqtt 
#pip3 install paho-mqtt
#pip3 install influxdb-client

MQTT_ERR_SUCCESS = 0
ALL_MQTT_TOPICS = "#"

def PubSub_onConnect(client, userdata, flags, rc):
    if (rc != 0):
        print("MQTT: Error connecting with result code {0}".format(rc))
    else:
        userdata.onMqttBrokerConnected()


def PubSub_onMessage(client, userdata, msg):
    #forward message to app instance in which the MQTT client lives  
    try:
        userdata.onMqttMessageReceived(msg.topic, msg.payload.decode())
    except Exception as e:
        print("MQTT: unhandled topic <{0}> received with payload {1} and error: {3}".format(msg.topic, msg.payload.decode(), e))


class mqttScanner:
    "MQTT scanner"
    def __init__(self, brokerIP, brokerPort, brokerKeepalive, blocking, onMessageCallback):
        self.mqttClient = {}
        self.brokerIP = brokerIP
        self.brokerPort = brokerPort
        self.brokerKeepalive = brokerKeepalive
        self.blocking = blocking
        self.onMessageCallback = onMessageCallback

        self.connect()
    
    def connect(self):
        print("MQTT: connecting to broker with IP address <{0}> via port {1}".format(self.brokerIP, self.brokerPort))

        #connect to MQTT broker
        self.mqttClient = mqtt.Client(userdata=self)
        self.mqttClient.on_connect = PubSub_onConnect
        self.mqttClient.on_message = PubSub_onMessage

        #connect to broker without exception in case the broker is not yet available or the network is not yet up
        self.mqttSaveConnect()
        #once the connected start the receive and send loop 
        if (self.blocking == True):
            self.mqttClient.loop_forever()    #blocking call with automatic reconnects
        else:
            self.mqttClient.loop_start()    #blocking call with automatic reconnects

    def mqttSaveConnect(self):
        try:
            self.mqttClient.connect(self.brokerIP, self.brokerPort, self.brokerKeepalive)
        except Exception as e:
            print("MQTT: Fundamental error: {0}".format(e))
            print("MQTT: Trying to connect...")
            time.sleep(1)
            self.mqttSaveConnect()

    def onMqttMessageReceived(self, topic, payload):
        #print("MQTT: Topic <{0}> received with payload {1}".format(topic, payload))
        try:
            self.onMessageCallback(topic, payload)
        except Exception as e:
            print("MQTT: calling onMessageCallback function failed with error <{0}>".format(e))
    
    def onMqttBrokerConnected(self):
        print("MQTT: Connected to broker at: <{0}>".format(self.brokerIP))    #this print() is necessary so that the following code is executed - no idea why?

        #subscribe to all topics the app wants to consume
        print("MQTT: subsribing to all topics")    
        retSubscribe = MQTT_ERR_SUCCESS
        mid = 0 #mid ...message id
        try:
            retSubscribe, mid = self.mqttClient.subscribe(ALL_MQTT_TOPICS)        
            if (retSubscribe != MQTT_ERR_SUCCESS):
                print("MQTT: Bad return code when subscribing to all topics: {0}".format(retSubscribe))

        except Exception as e:
            print("MQTT: Error subscribing to all topics: {0}".format(e))
        
        #subscription failed -> try again
        if (retSubscribe != MQTT_ERR_SUCCESS):
            print("MQTT: Trying to subscribe again...")
            time.sleep(1)
            self.onMqttBrokerConnected()
