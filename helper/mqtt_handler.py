#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import paho.mqtt.client as mqtt 
#pip3 install paho-mqtt
#pip3 install influxdb-client

MQTT_ERR_SUCCESS = 0

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


class mqttHandler:
    "MQTT handler"
    def __init__(self, brokerIP, brokerPort, brokerKeepalive, blocking, onMessageCallback):
        self.mqttClient = {}
        self.brokerIP = brokerIP
        self.brokerPort = brokerPort
        self.brokerKeepalive = brokerKeepalive
        self.blocking = blocking
        self.onMessageCallback = onMessageCallback
        self.subscriptionList = dict()          #[topic] = data object
        self.publicationList = dict()     #[topic] = data object

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
        self.subscribe()

    def subscribe(self):
        #subscribe to all topics the app wants to consume
        print("MQTT: subscribing to topics")    
        retSubscribe = MQTT_ERR_SUCCESS
        mid = 0 #mid ...message id
        for topic in self.subscriptionList:
            try:
                retSubscribe, mid = self.mqttClient.subscribe(topic)        
                if (retSubscribe != MQTT_ERR_SUCCESS):
                    print("MQTT: Bad return code when subscribing to topic <{0}>: {1}".format(topic, retSubscribe))
                    break

            except Exception as e:
                print("MQTT: Error subscribing to topic <{0}>: {1}".format(topic, e))
        
        #subscription failed -> try again
        if (retSubscribe != MQTT_ERR_SUCCESS):
            print("MQTT: Trying to subscribe again...")
            time.sleep(1)
            self.subscribe()


    def addSubscription(self, topic, destinationDataObj):
        #MQTT
        self.subscriptionList[topic] = destinationDataObj   #register topic and the destination data object to which all receive data will be mapped
        self.subscribe()
        
    def addPublication(self, topic, sourceDataObj):
        #MQTT
        self.publicationList[topic] = sourceDataObj

    def publish(self):
        #walk through all topics registered for cyclic publishing
        for topic in self.publicationList:
            try:
                sourceDataObj = self.publicationList[topic]
                #self.subscriptionList[topic] ...source data instance its data need to be published
                #key                          ...name of attribute in instance
                #jsonObj[key]                 ...value to be read from attribute
                self.mqttClient.publish(topic, json.dumps(sourceDataObj.__dict__))
                #print(json.dumps(sourceDataObj.__dict__))
    
            except Exception as e:
                print("MQTT: Error publishing topic <{0}>: {2}".format(topic, e))

