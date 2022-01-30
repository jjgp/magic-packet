PLATFORM  ?= linux/amd64

repository = jjgp/magic-packet
sha        = $(shell git rev-parse --short HEAD)

.PHONY: Dockerfile
Dockerfile:
	docker build --platform $(PLATFORM) \
		-t $(repository):$(sha) \
		-f Dockerfile \
		$(abspath ..)

.PHONY: devel.Dockerfile
devel.Dockerfile: %.Dockerfile:
	docker build --platform $(PLATFORM) \
		-t $(repository):$(sha)-$* \
		-f $@ \
		$(abspath ..)/environment/linux
