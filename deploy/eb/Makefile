ENVFILE     ?= .env
PLATFORM    ?= docker-20.10.7-ce
REGION      ?= us-east-1

include $(ENVFILE)
envvars      = $(shell sed 's/=.*//' $(ENVFILE))
export $(envvars)

comma        = ,
eb_app_name  = magic-packet
eb_env_name  = magic-packet-env
eb_env_cname = $(shell aws elasticbeanstalk describe-environments \
	--environment-names $(eb_env_name) \
	--no-include-deleted \
	--query "Environments[*].CNAME" \
	--output text)
space        = $(subst ,, )
envpairs     = $(subst $(space),$(comma),$(foreach v,$(envvars),$(v)="$($(v))"))

.PHONY: help
help:
	@echo "make create:\n    eb create $(eb_env_name) --envars $(envpairs)\n"
	@echo "make deploy:\n    steps using eb to deploy app and environment\n"
	@echo "make open:\n    eb open\n"
	@echo "make init:\n    eb init -r $(REGION) -p $(PLATFORM) $(eb_app_name)\n"
	@echo "make local_run:\n    eb local run --envvars $(envpairs)\n"
	@echo "make local_open:\n    eb local open\n"
	@echo "make platform_select:\n    eb platform select\n"
	@echo "make set_client_api_proxy:\n    eb set_env CLIENT_API_PROXY=...\n"
	@echo "make ssl_certificate:\n    create an ssl certificate for HTTPS\n"
	@echo "make terminate:\n    eb terminate --all\n"

.PHONY: create
create:
	@eb create $(eb_env_name) --envvars $(envpairs)

.PHONY: deploy
deploy: | init platform_select create set_client_api_proxy

.PHONY: open
open:
	@eb open

.PHONY: init
init:
	@eb init -r $(REGION) -p $(PLATFORM) $(eb_app_name)

.PHONY: local_run
local_run:
	@eb local run --envvars $(envpairs) CLIENT_API_PROXY=http://localhost:$(UVICORN_PORT)

.PHONY: local_open
local_open:
	@eb local open

.PHONY: platform_select
platform_select:
	@eb platform select

.PHONY: set_client_api_proxy
set_client_api_proxy:
	@$(eb_env_cname) | xargs -I {} eb setenv CLIENT_API_PROXY={}

# The SSL certificate is used to terminate HTTPS at the load balancer.
# To setup HTTPS reference: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-elb.html
.PHONY: ssl_certificate
ssl_certificate: PRIVATE_KEY_DIR ?= ~/.ssh
ssl_certificate: PRIVATE_KEY_NAME ?= $(eb_app_name)-deploy
ssl_certificate: PRIVATE_KEY_PREFIX := $(PRIVATE_KEY_DIR)/$(PRIVATE_KEY_NAME)
ssl_certificate:
	openssl genrsa 2048 > $(PRIVATE_KEY_PREFIX).pem
	@$(eb_env_cname) | xargs -I {} eb setenv CLIENT_API_PROXY={} \
		| xargs -I {} openssl req -new \
		-key $(PRIVATE_KEY_PREFIX).pem \
		-out $(PRIVATE_KEY_PREFIX)-csr.pem \
		-subj "/C=US/ST=Michigan/L=Detroit/O=Magic Packet/OU=Magic Packet/CN={}"
	openssl x509 -req -days 365 \
		-in $(PRIVATE_KEY_PREFIX)-csr.pem \
		-signkey $(PRIVATE_KEY_PREFIX).pem \
		-out $(PRIVATE_KEY_PREFIX).crt
	rm $(PRIVATE_KEY_PREFIX)-csr.pem

.PHONY: terminate
terminate:
	@eb terminate --all
