#https://docs.docker.com/engine/reference/builder/
#docker build --rm -t pymqttsample:1.0.0 .
#docker save -o pymqttsample-1-0-0.tar pymqttsample:1.0.0
#docker run -d --rm --network host -e MQTT_BROKER_IP=192.168.1.100 -e MQTT_BROKER_PORT=1883 --name pymqttsample-app pymqttsample:1.0.0
#docker logs pymqttsample-app
#docker container stop pymqttsample-app



FROM python:3-alpine

ADD . /
ADD main.py /

RUN pip3 install asyncio
RUN pip3 install paho-mqtt


#start python with unbuffered output option to see print outputs in docker log
CMD [ "python", "-u", "main.py" ]