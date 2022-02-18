ENVFILE         ?= .env
PLATFORM        ?= docker-20.10.7-ce
PRIVATE_KEY_DIR ?= ~/.ssh
REGION          ?= us-east-1

include $(ENVFILE)
envvars          = $(shell sed 's/=.*//' $(ENVFILE))
export $(envvars)

comma              = ,
eb_app_name        = magic-packet
eb_env_name        = magic-packet-env
eb_env_cname       = aws elasticbeanstalk describe-environments \
	--environment-names $(eb_env_name) \
	--no-include-deleted \
	--query "Environments[*].CNAME" \
	--output text
private_key_prefix = $(PRIVATE_KEY_DIR)/$(eb_app_name)-deploy
space              = $(subst ,, )
envpairs           = $(subst $(space),$(comma),$(foreach v,$(envvars),$(v)="$($(v))"))

.PHONY: help
help:
	@echo "make create:\n    eb create $(eb_env_name) --envars $(envpairs)\n"
	@echo "make deploy:\n    steps using eb to deploy app and environment\n"
	@echo "make open:\n    eb open\n"
	@echo "make init:\n    eb init -r $(REGION) -p $(PLATFORM) $(eb_app_name)\n"
	@echo "make local_run:\n    eb local run --envvars $(envpairs)\n"
	@echo "make local_open:\n    eb local open\n"
	@echo "make platform_select:\n    eb platform select\n"
	@echo "make set_client_api_proxy:\n    eb set_env REACT_APP_API_PROXY=...\n"
	@echo "make ssl_certificate:\n    create an ssl certificate for HTTPS\n"
	@echo "make terminate:\n    eb terminate --all\n"

.PHONY: create
create:
	@eb create $(eb_env_name) \
		-it c5.4xlarge,c5n.4xlarge \
		--envvars $(envpairs)

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
	@eb local run --envvars $(envpairs) REACT_APP_API_PROXY=http://localhost:$(UVICORN_PORT)

.PHONY: local_open
local_open:
	@eb local open

.PHONY: platform_select
platform_select:
	@eb platform select

.PHONY: set_client_api_proxy
set_client_api_proxy:
	@$(eb_env_cname) | xargs -I {} eb setenv REACT_APP_API_PROXY={}

# The SSL certificate is used to terminate HTTPS at the load balancer.
# To setup HTTPS reference: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https-elb.html
# As of now, adding the listener is a manual process.
# TODO: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options-general.html#command-options-general-elbv2-listener
.PHONY: ssl_certificate
ssl_certificate:
	@openssl genrsa 2048 > $(private_key_prefix).pem
	@$(eb_env_cname) | xargs -I {} openssl req -new \
		-key $(private_key_prefix).pem \
		-out $(private_key_prefix)-csr.pem \
		-subj "/C=US/ST=Michigan/L=Detroit/O=Magic Packet/OU=Magic Packet/CN={}"
	@openssl x509 -req -days 365 \
		-in $(private_key_prefix)-csr.pem \
		-signkey $(private_key_prefix).pem \
		-out $(private_key_prefix).crt
	@rm $(private_key_prefix)-csr.pem

.PHONY: import_certificate
import_certificate:
	@aws acm import-certificate \
		--certificate fileb://$(private_key_prefix).crt \
		--private-key fileb://$(private_key_prefix).pem \
		--tags Key=$(eb_env_name)

.PHONY: terminate
terminate:
	@eb terminate --all
