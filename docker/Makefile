PLATFORM ?= linux/amd64

sha       = $(shell git rev-parse --short HEAD)

.PHONY: magic-packet
magic-packet: Dockerfile
	docker build --platform $(PLATFORM) -t magic-packet:$(sha) -f Dockerfile $(abspath ..)
