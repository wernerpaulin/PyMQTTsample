#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import json
from helper.env_support import initializeENV
from helper.mqtt_handler import mqttHandler


#check for environmental variables in case this app is started in a docker container
MQTT_BROKER_IP = initializeENV("MQTT_BROKER_IP", "localhost")
MQTT_BROKER_PORT = int(initializeENV("MQTT_BROKER_PORT", 1883))
MQTT_BROKER_KEEPALIVE = int(initializeENV("MQTT_BROKER_KEEPALIVE", 60))

CYCLE_TIME_APP = initializeENV("CYCLE_TIME_APP", 0.2)

TOPIC_PARAMETER = "pymqttsample.lenze.mosaiq/parameter"
TOPIC_MONITOR = "pymqttsample.lenze.mosaiq/monitor"


def OnMessageReceivedMQTT(topic, payload):
    #print("OnMessageMQTT: Topic <{0}> received with payload {1}".format(topic, payload))

    #assume data is sent as JSON string: "{"actVelocity":"0.0"}"
    try:
        jsonObj = json.loads(payload)
        #map json key values directly to class instance
        for key in jsonObj:
            print( "JSON Object: key: {0}, value: {1}".format(key, jsonObj[key]) )
            #topic                        ...topic
            #key                          ...key / variable
            #jsonObj[key]                 ...value
            setattr(MyMqttHandler.subscriptionList[topic], key, jsonObj[key])    


    #ok, obviously not a JSON object (the "Pythonic" philosophy for this kind of situation is called EAFP, for Easier to Ask for Forgiveness than Permission.)
    except Exception as e:
        print("OnMessageMQTT: Topic <{0}>: error when interpreting payload <{1}>. Error: {2}".format(topic, payload, e))


class subscriptionData:
    def __init__(self):
        self.threshold = 100
        self.step = 1

class publicationData:
    def __init__(self):
        self.value = 0

SubData = subscriptionData()
PubData = publicationData()

MyMqttHandler = mqttHandler(brokerIP=MQTT_BROKER_IP, brokerPort=MQTT_BROKER_PORT, brokerKeepalive=MQTT_BROKER_KEEPALIVE, blocking=False, onMessageCallback=OnMessageReceivedMQTT)

async def TimeSlice(cycleTime):
    #initialization
    #initiate MQTT connection
    MyMqttHandler.addSubscription(TOPIC_PARAMETER, SubData)
    MyMqttHandler.addPublication(TOPIC_MONITOR, PubData)
    
    #enter cyclic execution
    while True:
        await asyncio.sleep(cycleTime)

        #saw tooth generator
        PubData.value = PubData.value + abs(SubData.step)
        if (PubData.value >= abs(SubData.threshold)):
            PubData.value = 0

        #publish generated values
        MyMqttHandler.publish()




""" CYCLIC SYSTEM """
try:

    """ START CYCLIC EXECUTION """
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(TimeSlice(CYCLE_TIME_APP))
    loop.run_forever()

except Exception as e:
    print("Event loop failed: {0}".format(e))
    
finally:
    print("Event loop stopped")
    loop.close()
