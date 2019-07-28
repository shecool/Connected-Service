import configparser
from datetime import datetime
import subprocess
import sys
import paho.mqtt.client as mqtt
import xml.etree.ElementTree as ET
import re
import requests
import json
from requests.auth import HTTPBasicAuth

ANALYZING = False

# Retrieve credentials
def get_credentials():
    cp = configparser.ConfigParser()
    try:
        cp.read('credentials.ini')
        mv_serial = cp.get('sense', 'serial')
        mv_zone = cp.get('sense', 'zone')
        endpoint_ip = cp.get('endpoint', 'EndpointIPAddress')
        endpoint_user = cp.get('endpoint', 'kiosk_user')
        endpoint_pass = cp.get('endpoint', 'kiosk_pass')
        mqtt_server = cp.get('mqtt', 'mqtt_server')
        mqtt_port = cp.get('mqtt', 'mqtt_port')
    except:
        print('Missing credentials or incorrect input file.')
        exit(1)
    return mv_serial, mv_zone, endpoint_ip, endpoint_user, endpoint_pass, mqtt_server, mqtt_port

# Print connection result code and subscribe to MV zone topic
def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    print('###############################################')
    serial = userdata['mv_serial']
    zone = userdata['mv_zone']
    client.subscribe('/merakimv/' + serial + '/' + zone)

# When an MQTT publish message is received, print update and analyze for people
def on_message(client, userdata, msg):
    datum = str(msg.payload)
    analyze(datum, userdata)

# Generic parse function
def parse(text, beg_tag, end_tag, beg_pos=0, end_pos=-1):
    if text.find(beg_tag, beg_pos, end_pos) == -1:
        return ('', -1)
    else:
        initial = text.find(beg_tag, beg_pos, end_pos) + len(beg_tag)
    if text.find(end_tag, initial) == -1:
        return ('', -1)
    else:
        final = text.find(end_tag, initial)

    return (text[initial:final], final+len(end_tag))

# Determine the current status of our service kiosk endpoint
def get_kiosk_status(endpoint_ip, endpoint_user, endpoint_pass, headers):
    response = requests.get(endpoint_ip + '/getxml?location=status/Call', auth=HTTPBasicAuth(endpoint_user, endpoint_pass),  headers=headers)
    root = ET.fromstring(response.content)
    return root

# Analyze MQTT and initiate call if people are detected.
def analyze(datum, userdata):
    global ANALYZING
    datum = str(datum)
    count = int(parse(datum, '{"person":', '}}')[0])

    # Analyze if people are detected
    # Only continue if we are not already in the image recognition process
    # This will avoid calling our image recognition/calling script multiple overlapping times
    if count > 0 and ANALYZING is False:
        # Print message
        plural = 'person' if count == 1 else 'people'
        message = f'{count} {plural} seen by MV camera!'
        print(message)

        # Get kiosk calling status
        headers_kiosk = {'content-type': 'text/xml'}
        endpoint_ip = userdata['endpoint_ip']
        endpoint_user = userdata['endpoint_user']
        endpoint_pass = userdata['endpoint_pass']
        root = get_kiosk_status(endpoint_ip, endpoint_user, endpoint_pass, headers_kiosk)

        # If the kiosk endpoint is not in a call, continue
        print("Detecting if kiosk is on a call.")
        if root.find('Call') is None:
            print("Kiosk is not on a call. Initiating image recognition process.")
            # Mark that we are currently going through the image recognition process
            ANALYZING = True

            # Run script to initiate people verification and service kiosk call
            # Once script is complete, value of ANALYZING should be returned as false
            ANALYZING = subprocess.call('python3 image_recog_calling.py', shell=True)
            ANALYZING = bool(ANALYZING)
        print('###############################################')

if __name__ == '__main__':
    # Get credentials
    (mv_serial, mv_zone, endpoint_ip, endpoint_user, endpoint_pass, mqtt_server, mqtt_port) = get_credentials()
    user_data = {
        'mv_serial': mv_serial,
        'mv_zone': mv_zone,
        'endpoint_ip': endpoint_ip,
        'endpoint_user': endpoint_user,
        'endpoint_pass': endpoint_pass,
        'mqtt_server': mqtt_server,
        'mqtt_port': mqtt_port,

    }

    # Start MQTT client
    try:
        client = mqtt.Client()
        client.user_data_set(user_data)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(mqtt_server, int(mqtt_port), 300)
        # Run indefinitely and handle reconnects
        client.loop_forever()
    except:
         print('MQTT Connection failed')
         exit(1)