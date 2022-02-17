ENVFILE  ?= .env
PLATFORM ?= docker-20.10.7-ce
REGION   ?= us-east-1

include $(ENVFILE)
envvars   = $(shell sed 's/=.*//' $(ENVFILE))
export $(envvars)

app_name  = magic-packet
comma     = ,
env_name  = magic-packet-env
space     = $(subst ,, )
envpairs  = $(subst $(space),$(comma),$(foreach v,$(envvars),$(v)="$($(v))"))

.PHONY: help
help:
	@echo "make create:\n    eb create $(eb_env) --envars $(envpairs)\n"
	@echo "make open:\n    eb open\n"
	@echo "make init:\n    eb init -r $(REGION) -p $(PLATFORM) $(app_name)\n"
	@echo "make local_run:\n    eb local run --envvars $(envpairs)\n"
	@echo "make local_open:\n    eb local open\n"
	@echo "make platform_select:\n    eb platform select\n"
	@echo "make terminate:\n    eb terminate --all\n"

.PHONY: create
create:
	@eb create $(env_name) --envvars $(envpairs)

.PHONY: open
open:
	@eb open

.PHONY: init
init:
	@eb init -r $(REGION) -p $(PLATFORM) $(app_name)

.PHONY: local_run
local_run:
	@eb local run --envvars $(envpairs)

.PHONY: local_open
local_open:
	@eb local open

.PHONY: platform_select
platform_select:
	@eb platform select

.PHONY: terminate
terminate:
	@eb terminate --all
