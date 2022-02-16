ENVFILE  ?= .env
PLATFORM ?= docker-20.10.7-ce
REGION   ?= us-east-1

include $(ENVFILE)
envvars   = $(shell sed 's/=.*//' $(ENVFILE))
export $(envvars)

app_name  = magic-packet
comma     = ,
eb        = cd ./eb && eb
eb_env    = magic-packet-env
space     = $(subst ,, )
envpairs  = $(subst $(space),$(comma),$(foreach v,$(envvars),$(v)="$($(v))"))

.PHONY: help
help:
	@echo "make client_build:\n    build static files\n"
	@echo "make client_init:\n    install client dependencies\n"
	@echo "make client_start:\n    start client\n"
	@echo "make content:\n    prepare app content\n"
	@echo "make eb_create:\n    eb create $(eb_env) --envars $(envpairs)\n"
	@echo "make eb_open:\n    eb open\n"
	@echo "make eb_init:\n    eb init -r $(REGION) -p $(PLATFORM) $(app_name)\n"
	@echo "make eb_local_run:\n    eb local run --envvars $(envpairs)\n"
	@echo "make eb_local_open:\n    eb local open\n"
	@echo "make eb_terminate:\n    eb terminate --all\n"
	@echo "make uvicorn_api:\n    start api server\n"
	@echo "make uvicorn_app:\n    start app server\n"
	@echo "make run_devel:\n    start client and api server (make -j2 run_devel)\n"

.PHONY: client_build
client_build: PUBLIC_URL ?= /
client_build:
	@PUBLIC_URL=$(PUBLIC_URL) npm --prefix client run build

.PHONY: client_init
client_init:
	@npm --prefix client i

.PHONY: client_start
client_start:
	@npm --prefix client run start

content/multilingual_embedding:
	@(cd content && curl -LO \
		https://github.com/harvard-edge/multilingual_kws/releases/download/v0.1-alpha/multilingual_context_73_0.8011.tar.gz \
		&& tar -xzf multilingual_context_73_0.8011.tar.gz \
		&& mv multilingual_context_73_0.8011.tar.gz multilingual_embedding \
		&& rm multilingual_context_73_0.8011.tar.gz)

content/multilingual_kws:
	@git -c advice.detachedHead=false clone \
		--depth=1 \
		--branch v0.1-alpha \
		https://github.com/harvard-edge/multilingual_kws \
		content/multilingual_kws

content/speech_commands:
	@(cd content && curl -LO \
		http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz \
		&& tar -xzf speech_commands_v0.02.tar.gz \
		&& mv speech_commands_v0.02 speech_commands \
		&& rm speech_commands_v0.02.tar.gz)

content/unknown_files:
	@(cd content && curl -L0 \
		https://github.com/harvard-edge/multilingual_kws/releases/download/v0.1-alpha/unknown_files.tar.gz \
		&& tar -xzf unknown_files.tar.gz \
		&& rm unknown_files.tar.gz)

.PHONY: content
content: content/multilingual_embedding content/multilingual_kws content/speech_commands

.PHONY: eb_create
eb_create:
	@$(eb) create $(eb_env) --envvars $(envpairs)

.PHONY: eb_open
eb_open:
	@$(eb) open

.PHONY: eb_init
eb_init:
	@$(eb) init -r $(REGION) -p $(PLATFORM) $(app_name)

.PHONY: eb_local_run
eb_local_run:
	@$(eb) local run --envvars $(envpairs)

.PHONY: eb_local_open
eb_local_open:
	@$(eb) local open

.PHONY: eb_terminate
eb_terminate:
	@$(eb) terminate --all

.PHONY: uvicorn
uvicorn_api:
	@uvicorn api.app:app

.PHONY: uvicorn_app
uvicorn_app:
	@uvicorn app:app

.PHONY: run_devel
run_devel: client_start uvicorn_api
