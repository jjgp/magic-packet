COMMON_VOICE_DIR    ?= cv-corpus-7.0-2021-07-21/en
DOCKERFILES          = $(shell find ./docker -type f -name "*.Dockerfile")
INFERENCE_SEQUENCE  ?= [0]
LEXICON_URL         ?= https://www.openslr.org/resources/11/librispeech-lexicon.txt
NUM_JOBS            ?= 8
REPOSITORY           = jjgp/magic-packet
MFA                 ?= docker run --platform linux/amd64 -it \
	-v $(abspath ./data):/opt/data \
	$(REPOSITORY):mfa \
	mfa
VOCAB               ?= ["fire"]

.PHONY: $(DOCKERFILES) generate_raw_audio_dataset help

help:
	@echo "make ./docker/%.Dockerfile       : docker build %.Dockerfile"
	@echo "make ./data/lexicon.txt          : download the lexicon"
	@echo "./data/raw/%/postive/aligned     : align raw audio dataset with mfa"
	@echo "make generate_raw_audio_dataset  : generate raw audio dataset with howl"

$(DOCKERFILES): ./docker/%.Dockerfile:
	docker build --platform linux/amd64 \
		-t $(REPOSITORY):$* \
		- < ./docker/$*.Dockerfile

./data/lexicon.txt:
	curl $(LEXICON_URL) -o $@

./data/raw/%/positive/aligned: ./data/lexicon.txt ./data/raw/%/positive/audio
	$(MFA) align --num_jobs $(NUM_JOBS) \
		/opt/data/raw/$*/positive/audio \
		/opt/data/lexicon.txt \
		english \
		/opt/data/raw/$*/positive/aligned

generate_raw_audio_dataset:
	docker run --platform linux/amd64 \
    	-v $(abspath ./data):/opt/data \
		-e VOCAB='$(VOCAB)' \
		-e INFERENCE_SEQUENCE='$(INFERENCE_SEQUENCE)' \
		-it $(REPOSITORY):howl \
		python -m training.run.generate_raw_audio_dataset \
		-i /opt/data/$(COMMON_VOICE_DIR) \
		-o /opt/data/raw \
		--positive-pct 100 \
		--negative-pct 5
