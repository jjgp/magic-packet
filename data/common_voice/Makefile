COMMON_VOICE_LANG  ?= en
COMMON_VOICE_VERS  ?= 7.0-2021-07-21
LEXICON_URL        ?= https://www.openslr.org/resources/11/librispeech-lexicon.txt
MFA_ACOUSTIC_MODEL ?= english
MFA_DIRECTORY      ?= ~/Documents/MFA
VOCAB              ?= hey fire fox

acoustic_model      = $(MFA_DIRECTORY)/pretrained_models/acoustic/$(MFA_ACOUSTIC_MODEL).zip
corpus_archive      = cv-corpus-$(COMMON_VOICE_VERS)-$(COMMON_VOICE_LANG).tar.gz
corpus_dir          = cv-corpus-$(COMMON_VOICE_VERS)/$(COMMON_VOICE_LANG)
splits_db           = $(corpus_dir)/splits.db
aligned_dir         = $(corpus_dir)/aligned
clips_dir           = $(corpus_dir)/clips
pythonpath          = $(abspath ../..)
python              = PYTHONPATH=$(pythonpath) python -m
magicpkt            = $(python) magic_packet.cli.magicpkt

.PHONY: help
help:
	@echo "make aligned:\n    mfa align audio clips\n"
	@echo "make $(corpus_archive):\n    download the corpus archive\n"
	@echo "make $(splits_db):\n    create the splits database\n"
	@echo "make extract:\n    extract clips of target vocab ($(VOCAB)) and OOV\n"

$(acoustic_model):
	mfa model download acoustic $(MFA_ACOUSTIC_MODEL)

.PHONY: aligned
aligned: N_JOBS ?= 8
aligned:
		$(magicpkt) common-voice align -j $(N_JOBS) \
		$(clips_dir) \
		lexicon.txt \
		english \
		$(aligned_dir) \
		--clean \
		--overwrite

$(corpus_archive):
	$(magicpkt) common-voice download \
		. \
		--language=$(COMMON_VOICE_LANG) \
		--version=$(COMMON_VOICE_VERS)

$(corpus_dir):
	mkdir -p $(corpus_dir)

$(splits_db): $(corpus_dir)
	$(magicpkt) common-voice createdb \
		./$(corpus_archive) \
		./$(splits_db) \
		-s train -s dev -s test

.PHONY: extract
extract: OOV_PCT ?= 5
extract:
	$(magicpkt) common-voice extract \
		./$(corpus_archive) \
		./$(splits_db) \
		./$(clips_dir) \
		--oov-pct $(OOV_PCT) \
		$(if $(VOCAB),$(foreach word,$(VOCAB),-v $(word)))

lexicon.txt:
	curl -L $(LEXICON_URL) -o $@
