# Connected-Service

Intelligently initate video calls based on a person's presense.


## Business/Technical Challenge

Many would agree there is nothing quite like a face to face conversation. Unfortunately, the world we live in today - one of agile changes and multidisciplinary teams - requires a proxy to human to human interaction effective enough to exchange thoughts, but quick enough to make adjustments at a moment's notice.  Video has proven to be an adept tool at connecting specialized teams to broader audiences, but many of the general public are to this day still coming to terms with leveraging video for frequent communications. Learning how to operate video endpoints may come with an unpredictably small or large learning curve, depending that individual's familiarity with video conferencing. This learning curve can introduce "friction" to one's willingness to interact with technology, often providing discouragement to the user and sometimes ending in total disengagement.

![Questioning](img/questioning.png)

Despite aesthetic improvements to the user interface - making the video platform more "user friendly", the broader idea of improving how people interact with technology becomes a problem with many potential solutions.

## Proposed Solution

Cisco has already created an amazing platform for video communications that resembles a true face to face conversation. While we have made great efforts to simply our user interface there still exist many people that hesitate to approach new technology. 

Our proposed solution leverages Meraki MV Camera's Sense API to detect when a person approaches a video endpoint and auto initiates a call to a remote destination. Thus, from a user’s perspective they simply have to walk up to a screen to be connected with a remote resource.


## Cisco Products Technologies/ Services

Our solution leverages the following Cisco technologies:

*  [WebEx Room Series](https://www.cisco.com/c/en/us/products/collaboration-endpoints/webex-room-series/index.html)
*  [Cisco Video Endpoint XAPI](https://www.cisco.com/c/dam/en/us/td/docs/telepresence/endpoint/)
*  [Meraki MV Sense API](https://developer.cisco.com/meraki/mv-sense/)


In addition our solution also leverages
*  [MQTT](https://developer.cisco.com/meraki/mv-sense/#!mqtt)
*  [Microsoft Cognitive Services API](https://azure.microsoft.com/en-ca/services/cognitive-services/)


## Team Members

* Samantha Yiu <cbogdon@cisco.com> - Trans PNC Enterprise Account
* Erik Lefebvre <eriklef@cisco.com> - Greater Pennsylvania Territory


## Solution Components

Our solution is comprised of 6 main components. The hardware is a Meraki MV Camera, Webex Video Endpoint.  three main components.  

The architecture is built around a microservices framework to demonstrate how multiple solutions can work together as long as there is a well defined API.   The overall architecture is shown below:

### Hardware
* Video Endpoints
* Meraki MV12 Camera
* CUCM Server

### API's Used
* Meraki MV Sense API
* [Meraki Snapshot API](https://developer.cisco.com/meraki/mv-sense/#!rest-api/snapshot)
* Azure Cognitive Services 
	* Face API

### Code
* [Python 3.7.3](https://www.python.org/)
	* MV MQTT (https://github.com/shiyuechengineer/adventure-lab)

Video Endpoints
REST API (XML)

CUCM Server
Hunt Group
Video Endpoint Registration

Meraki MV12 Camera
MQTT Client
MV Sense API
Snapshot API

MQTT Broker Server
Ubuntu, Mosquitto

Ubuntu VM
Python script - parse info and take action!

Azure Cognitive Services 
Face API


![Architecture](img/architecture.png)

There are three main modules in the solution.   They are described below:

### Person/People detection
The mqtt_detect_people.py script starts the MQTT client, subscribes to the MV camera topic, checks if a person is present and if the video endpoint is not already on a call initates the calling script. 

The MQTT script performs the following functions:
1. Starts the MQTT client
2. Subscribes to MQTT Topic for the Meraki camera's zone
3. Parses the returned json for people
4. If people are found, it checks if the video endpoint is already on a call
5. If not already on a call initializes the calling script

### Calling
The image_recog_calling.py script grabs a snapshot of the current camera feed and submits it to Microsoft Cognitive Services to perform a double blind check and ensure the MV people detection is not a false positive. If there is indeed a person it initiates a call to the predefined hunt group.

The broker, will perform the following functions:
1. Wait for requests from the CE-API to provision a user
2. Validate any received requests against the security white-list database
3. Store the requests in an internal database for later tracking
4. Leverage the REST-API to initiate the actual provisioning process with the guest-update.
5. Wait for response from guest-update for a wifi password
6. Provide status updates to the end user in a WebEx Teams Room

## Usage

### Overall Flow

## Installation


## Setup

The credentials.ini file should be supplied with your own Meraki API, Microsoft Azure  detailed information and documentation can be provided in the following links:


## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE.md)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)
