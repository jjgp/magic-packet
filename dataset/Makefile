# Jupyter is broken with docker's implementation on QEMU
# https://tongfamily.com/2021/12/21/docker-on-apple-m1-break-on-jupyter-notebooks-switch-to-podman/
DOCKER     = podman
PROJECT    = magic-packet
REPOSITORY = jjgp
TAG        = dataset

.PHONY: clean Dockerfile notebook help push stop

Dockerfile:
	$(DOCKER) build --platform linux/amd64 \
		-t $(REPOSITORY)/$(PROJECT):$(TAG) \
		.

notebook:
	$(DOCKER) run --rm --platform linux/amd64 -it \
		-v $(PWD):/opt/notebooks \
		-p 8888:8888 \
		$(REPOSITORY)/$(PROJECT):$(TAG) \
		/bin/bash -c "\
		conda run -n dataset --no-capture-output \
		jupyter notebook \
		--notebook-dir=/opt/notebooks \
		--ip='*' \
		--port=8888 \
		--allow-root"

push:
	$(DOCKER) push $(REPOSITORY)/$(PROJECT):$(TAG)

stop:
	@$(DOCKER) stop $$($(DOCKER) ps | grep "$(REPOSITORY)/$(PROJECT)" | awk '{ print $$1 }')

help:
	@echo "make clean       : docker rmi image"
	@echo "make Dockerfile  : docker build image"
	@echo "make notebook    : docker run image"
	@echo "make push        : docker push image"
	@echo "make stop        : docker stop container"

clean:
	$(DOCKER) rmi $(shell $(DOCKER) images -q $(REPOSITORY)/$(PROJECT))
