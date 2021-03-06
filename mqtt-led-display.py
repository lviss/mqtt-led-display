#!/usr/bin/env python

import json
from sys import exit
import paho.mqtt.client as mqtt
import scrollphathd
from scrollphathd.fonts import font3x5
import threading
import datetime

# amount to dim the display at night
night_brightness_modifier = 0.5

scrollphathd.rotate(180)

MQTT_SERVER = '192.168.0.2'
MQTT_PORT = 1883
MQTT_TOPIC = 'devices/thermostat1/get'
SERVER_LOAD_TOPIC = 'devices/server/load'

# Set these to use authorisation
MQTT_USER = None
MQTT_PASS = None

last_temperature_received = ""
last_load_received = 0
pos_x = 0

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))

    client.subscribe(MQTT_TOPIC)
    client.subscribe(SERVER_LOAD_TOPIC)


def on_message(client, userdara, msg):
    # dim the display before 7am and after 7pm
    brightness_modifier = 1 if 7 <= datetime.datetime.now().hour <= 19 else night_brightness_modifier
    if msg.topic == MQTT_TOPIC:
        global pos_x
        payload = json.loads(msg.payload)
        print payload["actual_temperature"]
        last_temperature_received = str(payload["actual_temperature"])
        # display height is 7, save the bottom row for the graph
        scrollphathd.clear_rect(0,0,None,6) # None defaults to display size
        scrollphathd.write_string(last_temperature_received, brightness=0.5 * brightness_modifier, font=font3x5)
        scrollphathd.show()
    elif msg.topic == SERVER_LOAD_TOPIC:
        print msg.payload
        last_load_received = float(msg.payload)
        scrollphathd.clear_rect(0,6,None,1) # None defaults to disqlay size
        brightness = 0.5
        if last_load_received > 8.0:
            brightness = 1 
            last_load_received = 8
        load_bar_width = last_load_received/8.0*17
        scrollphathd.fill(brightness * brightness_modifier, int(17 - load_bar_width), 6, int(load_bar_width + 1), 1)
        scrollphathd.show()
	
scrollphathd.set_clear_on_exit()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if MQTT_USER is not None and MQTT_PASS is not None:
    print('Using username: {un} and password: {pw}'.format(un=MQTT_USER, pw='*' * len(MQTT_PASS)))
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)

client.connect(MQTT_SERVER, MQTT_PORT, 60)

client.loop_forever()
