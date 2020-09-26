# Websocket-Chatroom
### Livesite: http://chatroom.westus.cloudapp.azure.com/

(Hosted on [Microsft Azure](https://azure.microsoft.com/en-us/))

## About
Websocket-chatroom is an in-memory, websocket based, chatroom server. 

## [Server](src/server/README.md)
The websocket server is build entirely using [asyncio](https://docs.python.org/3/library/asyncio.html) and [websockets](https://websockets.readthedocs.io/en/stable/intro.html) in Python 3.8, and containerized using [Docker](https://www.docker.com/products/docker-desktop). 

To get started with the server, check out the more detailed readme in `src/server`.

Here are some of the essentials:
- [Python 3.8.2](https://www.python.org/downloads/release/python-382/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [GNU Make](https://www.gnu.org/software/make/)

## [Client](src/client/README.md)
The chat client is built using vanilla [JavaScript](https://www.javascript.com/), and containerized using [Docker](https://www.docker.com/products/docker-desktop) and [NGINX](nginx.com).

To get started with the client, check out the more detailed readme in `src/client`.
Here are some of the essentials:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
    - [NGINX Image](https://hub.docker.com/_/nginx)
- [GNU Make](https://www.gnu.org/software/make/)

## License
This Project is licensed under the MIT license. see `LICENSE.txt` for more information. 

## Contact
Rafael Bayer - rafibayer7@gmail.com 
- https://github.com/rafibayer/Websocket-Chatroom

## Acknowledgements
- [Microsft Azure](https://azure.microsoft.com/en-us/)
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [GNU](https://www.gnu.org/)
- [NGINX](nginx.com)
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
 