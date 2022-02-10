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

.PHONY: deploy.Dockerfile
deploy.Dockerfile: TARGET ?=
deploy.Dockerfile: %.Dockerfile:
	docker build --platform $(PLATFORM) \
		$(if $(TARGET),--target $(TARGET)) \
		-t $(repository):$(sha)-$*$(if $(TARGET),-$(TARGET)) \
		-f $@ \
		$(abspath ..)/deploy
