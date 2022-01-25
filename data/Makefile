COMMON_VOICE_LANG  ?= en
COMMON_VOICE_VERS  ?= 7.0-2021-07-21
LEXICON_URL        ?= https://www.openslr.org/resources/11/librispeech-lexicon.txt
MFA_ACOUSTIC_MODEL ?= english
MFA_DIRECTORY      ?= ~/Documents/MFA
VOCAB              ?= hey fire fox

acoustic_model      = $(MFA_DIRECTORY)/pretrained_models/acoustic/$(MFA_ACOUSTIC_MODEL).zip
corpus_archive      = cv-corpus-$(COMMON_VOICE_VERS)-$(COMMON_VOICE_LANG).tar.gz
corpus_dir          = cv-corpus-$(COMMON_VOICE_VERS)/$(COMMON_VOICE_LANG)
corpus_db           = $(corpus_dir)/splits.db
aligned_dir         = $(corpus_dir)/aligned
clips_dir           = $(corpus_dir)/clips
pythonpath          = $(abspath ..)
python              = PYTHONPATH=$(pythonpath) python -m
magicpkt            = $(python) magic_packet.cli.magicpkt
vocab_dirs          = $(foreach word,$(VOCAB),$(corpus_dir)/$(word))

.PHONY: help
help:
	@echo "make aligned:\n  mfa align audio clips\n"
	@echo "make $(corpus_archive):\n  download the corpus archive\n"
	@echo "make $(corpus_db):\n  create the courpus databse\n"
	@echo "make extract:\n  extract clips of target vocab ($(VOCAB)) and OOV\n"

$(acoustic_model):
	mfa model download acoustic $(MFA_ACOUSTIC_MODEL)

.PHONY: aligned
aligned: N_JOBS := 8
aligned:
	yes n | mfa align -j $(N_JOBS) \
		$(clips_dir) \
		lexicon.txt \
		english \
		$(aligned_dir) \
		--clean \
		--overwrite

$(corpus_archive):
	$(magicpkt) cv download \
		. \
		--lang=$(COMMON_VOICE_LANG) \
		--version=$(COMMON_VOICE_VERS)

$(corpus_dir):
	mkdir -p $(corpus_dir)

$(corpus_db): $(corpus_dir)
	$(magicpkt) cv createdb \
		./$(corpus_archive) \
		./$(corpus_db) \
		--overwrite \
		--splits train dev test

.PHONY: extract
extract: OOV_PCT := 5
extract:
	$(magicpkt) cv extract \
		./$(corpus_archive) \
		./$(corpus_db) \
		./$(clips_dir) \
		--oov-pct $(OOV_PCT) \
		$(if $(VOCAB),--vocab $(VOCAB))

lexicon.txt:
	curl $(LEXICON_URL) -o $@
