PORT=80
TEST_PATH=./tests
LOCAL_CONTAINER=rbayer/chatroom
CONTAINER_NAME=chatroom

.PHONY: local
	

# Deploy a local instance of chatroom container
local: build_local
	# ignore deletion failures with '-'
	-docker rm -f $(CONTAINER_NAME) 
	docker run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(LOCAL_CONTAINER)

# build local chatroom container
build_local:
	docker build -t $(LOCAL_CONTAINER) .

stop_local:
	docker rm -f $(CONTAINER_NAME)

# run all unitests in /tests
test:
	cd $(TEST_PATH) && python -m unittest
