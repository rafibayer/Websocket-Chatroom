# Websocket-Chatroom (Server)
### Livesite:  http://chatroom.westus.cloudapp.azure.com/
### Endpoint: ws://chatroom-ws.westus.cloudapp.azure.com/

(Hosted on [Microsft Azure](https://azure.microsoft.com/en-us/))

## About
This is the server for the Websocket-Chatroom. This server was created using asyncio and websockets for Python, and containerized using Docker. See [How It Works](#How-It-Works) for more details.

## How It Work
`server.py` defines a Server object using our configuration files. When this object is created, a Chatroom object is also created to handle the behavior of our chatroom. when `.start()` is called on the server, asyncio is used to serve our function `ws_handler_async()` as a websocket handler. This function essentially describes what to do with each new connection. `ws_handler_async()` sends information about the connection to the Chatroom, as well as all future messages from this client. 

`chatroom.py` describes how most client interactions are handled. There are several "handler" methods, such as `handle_connection()`, `handle_message()`, and `handle_disconnect()` that take information about the event and define the appropriate behavior and response. Some are handled in `chatroom.py`, while others are sent to other specialized handlers. 

### Contents Overview
- server
    - This directory contains the main functionality of the server and chatroom. 
        - `server.py`: Defines the Websocket server, main entrypoint to the program.
        - `chatroom.py`: Defines most chatroom behavior, stores chatroom state.
        - `user.py`: Defines User class, used to store information about connected clients.
        - `command_handler.py`: Defines recognition and behavior of chat commands.
        - `utils.py`: Defines utility functions such as logging used throughout the program.
        - `config_manager.py`: Defines ConfigManager class, used to manage `.yaml` config files.
- config
    - This directory contains subdirectories containing configuration data for different build contexts (ex. prod, local, test).
- tests (`$ make test`)
    - This directory contains unit tests that are run via a `Python unittest` command in `Makefile`
- Dockerfile (`$ docker build`)
    - This file is used by docker to build a container for our server. The base image of this container is `python:3.8`. This `Dockerfile` also defines arguments sent by our Makefile to manage constants and configuration.
- Makefile (`$ make`)
    - This file is used to define our build and deployment processes. This file also defines variables and constants consumed by other parts of the build, like our `Dockerfile`.

### Build And Deploy
- Prerequisites
    - Building 
        - [Docker Desktop](https://www.docker.com/products/docker-desktop)
        - [GNU Make](https://www.gnu.org/software/make/)
    - Deployment
        - [Microsft Azure VM](https://azure.microsoft.com/en-us/services/virtual-machines/) (Or similar enviornment)
        - [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
- Building
    1. Substitute `DOCKER_USER` in `Makefile` for your docker username.
    2. Ensure you are logged into docker in your shell (`$ docker login`)
    - Local Build:
        - `$ make build_local`
    - Production Build:
        - `$ make prod_build`
- Deployment
    1. Substitute `VM_USER`, `VM_ADDR`, and `KEY_PATH` in `Makefile`.
    - Local Deployment:
        - `$ make local`
    - Production Deployment
        - Docker engine must be installed and running on VM.
        - `$ make prod_deploy`



## Disclaimer
I am by no means an expert on back-end development, webservers, websockets, or DevOps. This project exists as a learning exercise for me, and a simple example for others to demonstrate a use of websockets. If you have any suggestions for improvement, feel free to reach out or open a PR.