PLATFORM  ?= linux/amd64

repository = jjgp/magic-packet
sha        = $(shell git rev-parse --short HEAD)

.PHONY: magic-packet
magic-packet: Dockerfile
	docker build --platform $(PLATFORM) \
		-t $(repository):$(sha) \
		-f Dockerfile \
		$(abspath ..)
