import configparser
import re
import sys
import requests
import time
import json
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

# Import credentials from seperate file
def get_credentials():
    cp = configparser.ConfigParser()
    try:
        cp.read('credentials.ini')
        api_key = cp.get('meraki', 'key')
        net_id = cp.get('meraki', 'network')
        m_api_url = cp.get('meraki', 'merakiApiUrl')
        mv_serial = cp.get('sense', 'serial')
        endpoint_ip = cp.get('endpoint', 'EndpointIPAddress')
        endpoint_user = cp.get('endpoint', 'kiosk_user')
        endpoint_pass = cp.get('endpoint', 'kiosk_pass')
        tel_number = cp.get('endpoint', 'HuntGroupPhoneNumber')
        cog_sub_key = cp.get('microsoft', 'MicrosoftCogApiKey')
        cog_api_url = cp.get('microsoft', 'MicrosoftCogApiUrl')
    except:
        print('Missing credentials or incorrect input file.')
        exit(1)
    return api_key, net_id, m_api_url, mv_serial, endpoint_ip, endpoint_user, endpoint_pass, tel_number, cog_sub_key, cog_api_url

# Return image from snapshot API.
def get_snapshot(api_key, net_id, api_url, mv_serial):
    headers_meraki = {  'X-Cisco-Meraki-API-Key': api_key  }
    meraki_snapshot_url = api_url + net_id + '/cameras/' + mv_serial + '/snapshot'
    response_meraki = requests.post(meraki_snapshot_url, headers=headers_meraki)
    results_meraki = json.dumps(response_meraki.json())
    to_python = json.loads(results_meraki)
    image_url = to_python['url']
    return image_url

# Send snapshot to cognitive services to detect faces.
def analyze_snapshot(cog_api_url, image_url, cog_sub_key):
    headers_cog = { 'Ocp-Apim-Subscription-Key': cog_sub_key }
    params = {
        'returnFaceId': 'true',
        }
    response = requests.post(cog_api_url, params=params, headers=headers_cog, json={"url": image_url})
    cog_results = json.dumps(response.json())
    return cog_results

# Log into the kiosk endpoint and initiate a call to the agent hunt group
def call_agents(tel_number, endpoint_ip, endpoint_user, endpoint_pass):
    headers = {'content-type': 'text/xml'}
    xml = '<Command><Dial><Number>' + tel_number + '</Number></Dial></Command>'
    requests.post(endpoint_ip + '/putxml', data=xml, auth=HTTPBasicAuth(endpoint_user, endpoint_pass),  headers=headers)

def main():
    # Get credentials
    (api_key, net_id, m_api_url, mv_serial, endpoint_ip, endpoint_user, endpoint_pass, tel_number, cog_sub_key, cog_api_url) = get_credentials()
    user_data = {
        'api_key': api_key,
        'net_id': net_id,
        'm_api_url': m_api_url,
        'mv_serial': mv_serial,
        'endpoint_ip': endpoint_ip,
        'endpoint_user': endpoint_user,
        'endpoint_pass': endpoint_pass,
        'tel_number': tel_number,
        'cog_sub_key': cog_sub_key,
        'cog_api_url': cog_api_url
    }
    print("Getting snapshot from MV camera.")
    # Grab a snapshot from the MV camera
    image_url = get_snapshot(api_key, net_id, m_api_url, mv_serial)

    # Wait before sending snapshot to cognitive. URL can take up to 5 seconds to fully load
    time.sleep(5)

    # Leverage cognitive services with snapshot image URL to detect if there are faces
    print("Analyzing snapshot for people.")
    cog_results = analyze_snapshot(cog_api_url, image_url, cog_sub_key)
    # If a face was detected by Cognitive services, log into the kiosk endpoint and dial the agent hunt group extension
    if 'faceId' in cog_results:
        print("People detected. Call will be initiated to agents.")
        call_agents(tel_number, endpoint_ip, endpoint_user, endpoint_pass)
        # Return false to mark this script has ran in full, and can be run again if people are detected again
        return False

if __name__ == '__main__':
    main()