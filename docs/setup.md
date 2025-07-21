# Setup

## MQTT Server

<pre> ```bash sudo apt update sudo apt install mosquitto ``` </pre>

### Optionnal : open mosquitto server to allow remote connexions

create a new configuration file for mosquitto

<pre> ```bash sudo touch /etc/mosquitto/conf.d/custom.conf sudo nano /etc/mosquitto/conf.d/custom.conf ``` </pre>

add the following configuration
<pre> ```bash listener 1883 allow_anonymous true ``` </pre>

### Optionnal : Install a remote MQTT visual GUI client 

Example : MQTTX see https://mqttx.app/downloads

## Paho-mqtt

<pre> ```bash sudo apt install python3-paho-mqtt ``` </pre>

## Optional

### PIP (if not already there)

<pre> ```bash sudo apt update sudo apt install python3-pip ``` </pre>