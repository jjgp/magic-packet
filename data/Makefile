COMMON_VOICE_LANG  ?= en
COMMON_VOICE_VERS  ?= 7.0-2021-07-21
LEXICON_URL        ?= https://www.openslr.org/resources/11/librispeech-lexicon.txt
MFA_ACOUSTIC_MODEL ?= english
MFA_DIRECTORY      ?= ~/Documents/MFA
VOCAB              ?= hey fire fox

corpus_archive      = cv-corpus-$(COMMON_VOICE_VERS)-$(COMMON_VOICE_LANG).tar.gz
corpus_dir          = cv-corpus-$(COMMON_VOICE_VERS)/$(COMMON_VOICE_LANG)
corpus_db           = $(corpus_dir).db
mfa                 = $(shell command -v mfa)
pythonpath          = $(abspath ..)
python              = PYTHONPATH=$(pythonpath) python -m

.PHONY: help
help:
	@echo "make $(corpus_archive):\n  download the common voice corpus archive\n"
	@echo "make $(corpus_db):\n  create the courpus databse\n"

$(corpus_archive):
	$(python) magic_packet.datasets.cv_corpus.download_archive \
		$(abspath .) \
		--lang=$(COMMON_VOICE_LANG) \
		--version=$(COMMON_VOICE_VERS)

$(corpus_db):
	$(python) magic_packet.datasets.cv_corpus.database.create_database \
		$(abspath $(corpus_archive)) \
		$(abspath $(corpus_db)) \
		--overwrite \
		--splits train dev test

$(corpus_dir):
	mkdir -p $(corpus_dir)

$(MFA_DIRECTORY)/pretrained_models/acoustic/$(MFA_ACOUSTIC_MODEL).zip:
	mfa model download acoustic $(MFA_ACOUSTIC_MODEL)

.PHONY: extract_clips
extract_clips:
	$(python) magic_packet.datasets.cv_corpus.vocab.extract_clips \
		$(abspath $(corpus_archive)) \
		$(abspath $(corpus_dir)) \
		$(abspath $(corpus_db)) \
		--vocab $(VOCAB)

# TODO: mfa model download is a dependency

# $(foreach word,$(VOCAB),$(corpus_dir)/$(word)):
# 	echo $(VOCAB)

# $(corpus_dir)/alignments: N_JOBS ?= 8
# $(corpus_dir)/alignments: $(corpus_dir) lexicon.txt
# 	yes n | $(mfa) align --num_jobs $(N_JOBS) \
# 		$(corpus_dir)/clips \
# 		lexicon.txt \
# 		english \
# 		$@

lexicon.txt:
	curl $(LEXICON_URL) -o $@
