.DEFAULT_GOAL := local

# Docker username
DOCKER_USER=rbayer
# Port to publish in docker run
PORT=80
# Path to tests relative to Makefile
TEST_PATH=./tests
# container name for local build
LOCAL_CONTAINER=$(DOCKER_USER)/chatroom_local
# container name for prod build
PROD_CONTAINER=$(DOCKER_USER)/chatroom_prod
# running container name
CONTAINER_NAME=chatroom
# path to local config files relative to Dockerfile
LOCAL_CONFIG_PATH=/config/local_config
# path to prod config files relative to Dockerfile
PROD_CONFIG_PATH=/config/prod_config

# SSH stuff
VM_USER=azureuser
VM_ADDR=chatroom-ws.westus.cloudapp.azure.com
KEY_PATH=~/.ssh/chatroom-vm_key.pem

# SSH into VM, pull latest container, remove old container, run new container, get logs
prod_deploy: prod_build
	ssh -i $(KEY_PATH) $(VM_USER)@$(VM_ADDR) -- "echo "ssh succeeded" && \
	docker pull $(PROD_CONTAINER):latest && \
	docker rm -f $(CONTAINER_NAME) 2> /dev/null || true && \
	docker run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) \
		--restart unless-stopped $(PROD_CONTAINER) && \
	docker logs $(CONTAINER_NAME)"

# build production container, push to dockerhub
prod_build:
	docker build --build-arg configpath=$(PROD_CONFIG_PATH) -t $(PROD_CONTAINER):latest .
	docker push $(PROD_CONTAINER):latest

# ssh into VM, docker logs container
prod_logs:
	ssh -i $(KEY_PATH) $(VM_USER)@$(VM_ADDR) -- "echo "ssh succeeded" && \
	docker logs $(CONTAINER_NAME)"

# ssh into VM, delete container
prod_stop:
	ssh -i $(KEY_PATH) $(VM_USER)@$(VM_ADDR) -- "echo "ssh succeeded" && \
	docker rm -f $(CONTAINER_NAME)"

# Remove old local container, run new local container
local: build_local
	# ignore deletion failures with '-'
	-docker rm -f $(CONTAINER_NAME) 
	docker run -d -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(LOCAL_CONTAINER)

# build local container
build_local:
	docker build --build-arg configpath=$(LOCAL_CONFIG_PATH) -t $(LOCAL_CONTAINER) .

# stop local instance of container
stop_local:
	docker rm -f $(CONTAINER_NAME)

# ssh into VM shortcut
ssh:
	ssh -i $(KEY_PATH) $(VM_USER)@$(VM_ADDR)

# run all unittests in /tests
test:
	cd $(TEST_PATH) && python -bm unittest