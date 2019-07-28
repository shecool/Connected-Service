# Connected-Service

Intelligently initate video calls based on a person's presense.


## Business/Technical Challenge

Many would agree there is nothing quite like a face to face converstation. Unfortuantely, the world we live in today - one of agile changes and multidisciplinary teams - requires a proxy to human to human interaction effective enough to exchange thoughts, but quick enough to make adjustments at a moment's notice.  Video has proven to be an adept tool at connecting specialized teams to broader audiences, but many of the general public are to this day still coming to terms with leveraging video for frequent communications. Learing how to operate video endpoints may come with an unpredictably small or large learning curve, depending that individual's familarity with video conferencing. This learning curve can introduce  "friction" to one's willingness to interact with technology, often providing discouragement to the user and sometimes ending in total disengagement.  

**Image for questioning**
![Questioning](img/questioning.png)

Despite aesthetic improvments to the user interface - making the video platform more "user friendly", the broader idea of improving how people interact with technology becomes a problem with many potential solutions.

## Proposed Solution

Cisco has already created an amazing platform for video communications that resembles a true face to face conversation. While we have made great efforts to simply our user interface there still exist many people that hesitate to approach new technology. 

Our proposed solution leverages Meraki MV Camera's Sense API to detect when a person approaches a video endpoint and auto initates a call to a remote destination. Thus, from a users perspective they simply have to walk up to a screen to be connected with a remote resource. 


### Cisco Products Technologies/ Services

Our solution leverages the following Cisco technologies:

*  [WebEx Room Series](https://www.cisco.com/c/en/us/products/collaboration-endpoints/webex-room-series/index.html)
*  [Cisco Video Endpoint XAPI](https://www.cisco.com/c/dam/en/us/td/docs/telepresence/endpoint/)
*  [Meraki MV Sense API](https://www.cisco.com/c/dam/en/us/td/docs/telepresence/endpoint/)

In addition our solution also leverages
*  [MQTT](https://developer.cisco.com/meraki/mv-sense/#!mqtt)
*  [Microsoft Cognitive Services API](https://azure.microsoft.com/en-ca/services/cognitive-services/)


## Team Members

* Samantha Yiu <cbogdon@cisco.com> - Trans PNC Enterprise Account
* Erik Lefebvre <eriklef@cisco.com> - Greater Pennsylvania Territory

## Solution Components

Our solution is comprised of 6 main components. The hardware is a Meraki MV Camera and a Webex Video Endpoint.  three main components.   The architecture is built around a microservices framework to demonstrate how multiple solutions can work together as long as there is a well defined API.   The overall architecture is shown below:

![Architecture](img/architecture.png)

There are three main modules in the solution.   They are described below:

### Person/People detection
The CEAPI module listens for provisioning requests from video endpoints.  When the "Network Registration"
button is pressed the endpoint will send an HTTP Feedback request to the CE API Service.  This service then
requests the broker to provision the account.  



The MQTT script performs the following functions:
1. Subscribes to MQTT Topic for the Meraki camera's zone
2. Parses the returned json for people
3. Sends a pop up confirmation back to the video endpoint
4. When the user confirms he/she would like an account provisioned the service with make a call to the Broker to have the request processed.
5. A confirmation message is sent to the Video endpoint so the user knows the process is underway.

### Calling
The broker is responsible for receiving requests from the CE-API to provision guest users.   It uses a database to whitelist both video endpoints and email domains to provide a very simple security mechanism.

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

* [CE-API](ceapi/README.md)
* [broker](broker/README.md)
* [guest-update](guest-update/README.md)


## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE.md)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)
