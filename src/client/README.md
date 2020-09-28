# Websocket-Chatroom (Client)
### Livesite: http://chatroom.westus.cloudapp.azure.com/

(Hosted on [Microsft Azure](https://azure.microsoft.com/en-us/))

## About
This is the client for the Websocket-Chatroom server. This client is created using HTML, CSS, and Vanilla JavaScript, and containerized using Docker with an NGINX base image. See [How It Works](#How-It-Works) for more details.

## How It Works
NGINX is an HTTP webserver that we use to serve the static content of our webpage. We deploy an NGINX server via a Docker image and `Dockerfile`, that packages the contents of our site and its resources into a container. This container has all of the resources required to run our server, so it is very portable, this allows us to easily update the contents of our remote VM using `$ docker push` and `$ docker pull`, much like a GitHub repository. 

`index.js` defines the main logic of our page and is quite simple. The entire body of this script is wrapped in a function that requires a single parameter "server_url", this variable is defined in `constants.js` (created at build time), and passed in at the bottom of `index.js`. This parameter is a URL and defines the websocket endpoint that our client should connect to. The connection is established, and event handlers are defined to handle sending and recieving messages via the client. Since our server defines a common json schema (`src/server/server/response.py`) for all outgoing messages, we can parse incoming messages and extract this data safely to decide how to render the message in our chat window. For example, we can give a "Private message" (origin == PRIVATE) a different look than a notification sent by the server (origin == SERVER).

### Contents Overview
- static
    - This directory contains the static elements of the website.
        - `index.html`: The main page
        - `Index.css`: Stylesheet for the main page
        - `Index.js`: JavaScript for the main page
- constants
    - This directory contains options for `constants.js` files to be copied over during the build process. This allows us to easily manage testing and production constants via our `Makefile`. 
- Configuration
    - Similar to constants, the `.conf` files are different configuration options for our NGINX (Local testing vs production).
- Dockerfile (`$ docker build`)
    - This file is used by docker to build a container for our client. The base image of this container is `NGINX`. This `Dockerfile` also defines arguments sent by our Makefile to manage constants and configuration.
- Makefile (`$ make`)
    - This file is used to define our build and deployment processes. This file also defines variables and constants consumed by other parts of the build, like our `Dockerfile`.

### Build and Deploy
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
I'm by no means an expert in front-end development. I probably could've spent time figuring out how to make a beautiful webapp using a framework like React or Angular, but that wasn't really the point of this project. Head on over to `../server` for more interesting stuff. That being said, if there are any good practices I'm missing here please let me know or even just make a PR :)
