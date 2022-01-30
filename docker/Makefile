PLATFORM  ?= linux/amd64

repository = jjgp/magic-packet
sha        = $(shell git rev-parse --short HEAD)
variants   = $(notdir $(shell find . -type f -name "*.Dockerfile"))

.PHONY: Dockerfile
Dockerfile:
	docker build --platform $(PLATFORM) \
		-t $(repository):$(sha) \
		-f Dockerfile \
		$(abspath ..)

.PHONY: $(variants)
$(variants): %.Dockerfile:
	docker build --platform $(PLATFORM) \
		-t $(repository):$(sha)-$* \
		-< $@
