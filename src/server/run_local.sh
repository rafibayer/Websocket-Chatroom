docker rm -f chatroom
docker run -d -p 80:80 --name chatroom rbayer/chatroom 