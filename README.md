# PyMQTTsample
Simple MQTT sample made in Python

<br />
Link to Repository: https://github.com/wernerpaulin/PyMQTTsample

<!-- APP SHIELDS -->
[![GitHub issues](https://img.shields.io/github/issues/wernerpaulin/PyMQTTsample)](https://github.com/wernerpaulin/PyMQTTsample/issues)
[![GitHub forks](https://img.shields.io/github/forks/wernerpaulin/PyMQTTsample)](https://github.com/wernerpaulin/PyMQTTsample/network)
[![GitHub stars](https://img.shields.io/github/stars/wernerpaulin/PyMQTTsample)](https://github.com/wernerpaulin/PyMQTTsample/stargazers)
[![GitHub license](https://img.shields.io/github/license/wernerpaulin/PyMQTTsample)](https://github.com/wernerpaulin/PyMQTTsample/blob/main/LICENSE)


<!-- APP LOGO -->
<br />
<p align="center">
  <a href="https://github.com/wernerpaulin/PyMQTTsample">
    <img src="images/icon.png" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">PyMQTTsample</h3>

  <p align="center">
    This app is written in Python® 3. It shows a simple implementation of MQTT for app handling demonstration.
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-app">About The App</a>
      <ul>
        <li><a href="#gallery">Gallery</a></li>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#communication">Communication</a>
      <ul>
        <li><a href="#interfaces">Interfaces</a></li>
        <li><a href="#published-ports">Ports Published By This App</a></li>
      </ul>
    </li>
    <li><a href="#data-management">Data Management</a></li>
      <ul>
        <li><a href="#environmental-variables">Environmental Variables</a></li>
        <li><a href="#volumes">Volumes</a></li>
      </ul>
    <li><a href="#information">Information</a></li>
    <li><a href="#legal-statemets">Legal Statements</a></li>
  </ol>
</details>

<!-- ABOUT THE APP -->
## About The App
### Gallery
<img src="images/gallery1.png" 
     alt="Gallery 1" 
     style="float:left; margin-right: 10px;" 
     width="200"/>

### Features
* tbd



### Built With
| Technology | Description |
| -------------- | ----------- |
| [Python®](https://www.python.org/) | asyncio for concurrent execution of coroutines |
| [Eclipse Paho®](https://www.eclipse.org/paho/) | MQTT client |
| [Docker®](https://www.docker.com/) | Container technology |


<!-- GETTING STARTED -->
## Getting Started

Find this app in the App Store and use it in a machine.

### Prerequisites

This app requires a MQTT broker which can either run as an app or on a different host but in the same network of the Runtime.
It also requires an influxdb app running on the Runtime or on a different host.

### Usage
1. tbd


<!-- COMMUNICATION -->
## Communication
### Interfaces
The app subscribes to the following topics:
| Topic | Value Example |
| -------------- | ----------- |
| mosaiq.lenze.pymqttsample/parameter | ``` "{"threshold": 200, "step": 1}" ``` |


The app publishes the following topics:
| Topic | Value Example |
| -------------- | ----------- |
| mosaiq.lenze.pymqttsample/monitor | ``` "{"value": 1}" ``` |

**Please note: Ports can be mapped to different host ports in the machine settings**

<!-- DATA MANAGEMENT -->
## Data Management

### Environmental Variables
Environmental variables are used to initialize or define a certain functionality of an app and can be changed in the machine settings:
| Variable | Default Value | Changeable by User | Description | 
| -------- | ------------- | ------------------ | ----------- |
| MQTT_BROKER_IP | mosaiq.eclipsemosquitto | yes | Hostname or IP address of MQTT broker | 
| MQTT_BROKER_PORT | 1883 | yes | Port used by the MQTT broker |
| MQTT_BROKER_KEEPALIVE | 60 | yes | Maximum time that this app does not communicate with the broker |

### Volumes
Mount points are access points to volumes (like paths) provided to the app to read and write data:

| Mount Point | Default Data | Changeable by User | Description | 
| -------- | ------------- | ------------------ | ----------- |
| n.a. | | |


<!-- INFORMATION -->
## Information
| Developer | Compatibility | Size on Runtime | Copyright | License |
| ----------| ------------- |---------------- | --------- | ------- |
| [Lenze SE](https://www.lenze.com/) | Requires Runtime 1.0 or later | 50.7 MB | © 2021- [Lenze SE](https://www.lenze.com/) | MIT License. See `LICENSE` for more information. |


## Legal Statements
* "Python®" and the Python logos are trademarks or registered trademarks of the Python Software Foundation.
* "Eclipse®", "Mosquitto®", Paho® and the respective logos are trademarks or registered trademarks of the Eclipse Foundation.
* "Docker®" and "Docker Hub®" are trademarks or registered trademarks of Docker.
