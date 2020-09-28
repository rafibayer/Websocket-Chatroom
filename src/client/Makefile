.DEFAULT_GOAL := local

DOCKER_USER=rbayer
# Port to publish in docker run for local
LOCAL_PORT=8080
# Port to publish in docker run for prod
PROD_PORT=80
# container name for local build
LOCAL_CONTAINER=$(DOCKER_USER)/chatroom_client_local
# container name for prod build
PROD_CONTAINER=$(DOCKER_USER)/chatroom_client_prod
# running container name
CONTAINER_NAME=chatroom_client
# path to local constants files relative to Dockerfile
LOCAL_CONFIG_PATH=/constants/local_constants.js
# path to prod constants files relative to Dockerfile
PROD_CONFIG_PATH=/constants/prod_constants.js
# path to local nginx config relative to Dockerfile
LOCAL_NGINX_PATH=local_default.conf
# path to prod nginx config relative to Dockerfile
PROD_NGINX_PATH=prod_default.conf

VM_USER=azureuser
VM_ADDR=chatroom.westus.cloudapp.azure.com

KEY_PATH=~/.ssh/chatroom-vm-client_key.pem

prod_deploy: prod_build
	ssh -i $(KEY_PATH) $(VM_USER)@$(VM_ADDR) -- "echo "ssh succeeded" && \
	docker pull $(PROD_CONTAINER):latest && \
	docker rm -f $(CONTAINER_NAME) 2> /dev/null || true && \
	docker run -d -p $(PROD_PORT):$(PROD_PORT) --name $(CONTAINER_NAME) \
		--restart unless-stopped $(PROD_CONTAINER) && \
	docker logs $(CONTAINER_NAME)"

prod_build:
	docker build \
	--build-arg build_const_path=$(PROD_CONFIG_PATH) \
	--build-arg port=$(PROD_PORT) \
	--build-arg nginx_config_path=$(PROD_NGINX_PATH) \
	-t $(PROD_CONTAINER):latest .
	docker push $(PROD_CONTAINER):latest

prod_logs:
	ssh -i $(KEY_PATH) $(VM_USER)@$(VM_ADDR) -- "echo "ssh succeeded" && \
	docker logs $(CONTAINER_NAME)"

prod_stop:
	ssh -i $(KEY_PATH) $(VM_USER)@$(VM_ADDR) -- "echo "ssh succeeded" && \
	docker rm -f $(CONTAINER_NAME)"

local: build_local
	-docker rm -f $(CONTAINER_NAME)
	docker run -d -p$(LOCAL_PORT):$(LOCAL_PORT) --name $(CONTAINER_NAME) $(LOCAL_CONTAINER)



build_local:
	docker build \
	--build-arg build_const_path=$(LOCAL_CONFIG_PATH) \
	--build-arg port=$(LOCAL_PORT) \
	--build-arg nginx_config_path=$(LOCAL_NGINX_PATH) \
	-t $(LOCAL_CONTAINER) .

local_no_cache: build_local_no_cache
	-docker rm -f $(CONTAINER_NAME)
	docker run -d -p$(LOCAL_PORT):$(LOCAL_PORT) --name $(CONTAINER_NAME) $(LOCAL_CONTAINER)

build_local_no_cache:
	docker build \
	--no-cache \
	--build-arg build_const_path=$(LOCAL_CONFIG_PATH) \
	--build-arg port=$(LOCAL_PORT) \
	--build-arg nginx_config_path=$(LOCAL_NGINX_PATH) \
	-t $(LOCAL_CONTAINER) .

# stop local instance of container
stop_local:
	docker rm -f $(CONTAINER_NAME)

# ssh into VM shortcut
ssh:
	ssh -i $(KEY_PATH) $(VM_USER)@$(VM_ADDR)
