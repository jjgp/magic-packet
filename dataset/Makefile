PROJECT    = magic-packet
REPOSITORY = jjgp
TAG        = dataset

.PHONY: clean Dockerfile notebook help push stop

Dockerfile:
	docker build --platform linux/amd64 \
		-t $(REPOSITORY)/$(PROJECT):$(TAG) \
		.

notebook:
	docker run --platform linux/amd64 -it \
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
	docker push $(REPOSITORY)/$(PROJECT):$(TAG)

stop:
	@docker stop $$(docker ps | grep "$(REPOSITORY)/$(PROJECT)" | awk '{ print $$1 }')

help:
	@echo "make clean       : docker rmi image"
	@echo "make Dockerfile  : docker build image"
	@echo "make push        : docker push image"
	@echo "make stop        : docker stop container"

clean:
	docker rmi $(shell docker images -q $(REPOSITORY)/$(PROJECT))
