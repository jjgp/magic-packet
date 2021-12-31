PROJECT    = magic-packet
REPOSITORY = jjgp
TAG        = howl

.PHONY: clean Dockerfile help push stop

Dockerfile:
	docker build --platform linux/amd64 \
		-t $(REPOSITORY)/$(PROJECT):$(TAG) \
		- < Dockerfile

push:
	docker push $(REPOSITORY)/$(PROJECT):$(TAG)

help:
	@echo "make Dockerfile  : docker build image"
	@echo "make push        : docker push image"
