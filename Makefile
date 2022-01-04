COMMON_VOICE_DIRNAME       ?= cv-corpus-7.0-2021-07-21/en
DOCKER_PLATFORM            ?= linux/amd64
HOWL_PATH                  ?=
LEXICON_URL                ?= https://www.openslr.org/resources/11/librispeech-lexicon.txt
NUM_JOBS                   ?= 8
VOCAB                      ?= fire

data_abspath                = $(abspath ./data)
raw_abspath                 = $(data_abspath)/raw
dockerfiles                 = $(shell find ./docker -type f -name "*.Dockerfile")
mfa                         = $(shell command -v mfa)
negative_abspath	        = $(raw_abspath)/$(VOCAB)/negative
inference_sequence          = '[$(shell seq -s, 0 $(shell grep -o '_' <<<$(1) | grep -c .) | sed s'/,$$//')]'
positive_abspath	        = $(raw_abspath)/$(VOCAB)/positive
positive_alignment_abspath  = $(positive_abspath)/alignment
repository                  = jjgp/magic-packet
vocab_sequence              = '["$(shell sed 's/_/","/g' <<<$(1))"]'

ifeq ($(mfa),)
mfa                         = docker run --platform $(DOCKER_PLATFORM) -it \
	-v $(data_abspath):$(data_abspath) \
	$(repository):mfa \
	mfa
endif

ifeq ($(HOWL_PATH),)
	howl_context            = docker run --platform $(DOCKER_PLATFORM) \
    	-v $(data_abspath):$(data_abspath) \
		-it $(repository):howl
else
	howl_context            = cd $(HOWL_PATH) &&
endif

.PHONY: help
help:
	@echo "make ./data/lexicon.txt          : download the lexicon"
	@echo "make ./docker/%.Dockerfile       : docker build %.Dockerfile"
	@echo "make attach_positive_alignment   : create aligned metadata files"
	@echo "make generate_raw_audio_dataset  : create positive/negative samples and metadata"
	@echo "make positive_alignment          : mfa align positive samples"
	@echo "make stitch_vocab_samples        : stitch aligned positive samples"
	@echo "make stub_negative_alignment     : mock align negative samples"

./data/lexicon.txt:
	curl $(LEXICON_URL) -o $@

.PHONY: $(dockerfiles)
$(dockerfiles): ./docker/%.Dockerfile:
	docker build --platform $(DOCKER_PLATFORM) -t $(repository):$* - < ./docker/$*.Dockerfile

.PHONY: attach_positive_alignment
attach_positive_alignment: $(positive_alignment_abspath)
	@($(howl_context) python -m training.run.attach_alignment \
		--input-raw-audio-dataset $(positive_abspath) \
  		--token-type word \
  		--alignment-type mfa \
  		--alignments-path $(positive_alignment_abspath))

.PHONY: generate_raw_audio_dataset
generate_raw_audio_dataset: common_voice_abspath := $(data_abspath)/$(COMMON_VOICE_DIRNAME)
generate_raw_audio_dataset: $(common_voice_abspath)
	@($(howl_context) env VOCAB=$(call vocab_sequence,$(VOCAB)) \
		INFERENCE_SEQUENCE=$(call inference_sequence,$(VOCAB)) \
		python -m training.run.generate_raw_audio_dataset \
		-i $(common_voice_abspath) \
		-o $(raw_abspath) \
		--positive-pct 100 \
		--negative-pct 5)

.PHONY: positive_alignment
positive_alignment: lexicon_abspath        := $(data_abspath)/lexicon.txt
positive_alignment: positive_audio_abspath := $(positive_abspath)/audio
positive_alignment: $(lexicon_abspath) $(positive_audio_abspath)
	@$(mfa) align --num_jobs $(NUM_JOBS) \
		$(positive_audio_abspath) \
		$(lexicon_abspath) \
		english \
		$(positive_alignment_abspath)

.PHONY: stitch_vocab_samples
stitch_vocab_samples: $(addprefix $(positive_abspath)/aligned-metadata-,$(addsuffix .jsonl, dev test training))
	@($(howl_context) env VOCAB=$(call vocab_sequence,$(VOCAB)) \
		INFERENCE_SEQUENCE=$(call inference_sequence,$(VOCAB)) \
		python -m training.run.stitch_vocab_samples \
		--aligned-dataset $(positive_abspath) \
		--stitched-dataset $(positive_abspath)/stitched)

.PHONY: stub_negative_alignment
stub_negative_alignment: $(negative_abspath)
	@($(howl_context) python -m training.run.attach_alignment \
		--alignment-type stub \
		--input-raw-audio-dataset $(negative_abspath) \
		--token-type word
