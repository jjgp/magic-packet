COMMON_VOICE_LANG  ?= en
COMMON_VOICE_VERS  ?= 7.0-2021-07-21
LEXICON_URL        ?= https://www.openslr.org/resources/11/librispeech-lexicon.txt
MFA_ACOUSTIC_MODEL ?= english
MFA_DIRECTORY      ?= ~/Documents/MFA
VOCAB              ?= hey fire fox

acoustic_model      = $(MFA_DIRECTORY)/pretrained_models/acoustic/$(MFA_ACOUSTIC_MODEL).zip
corpus_archive      = cv-corpus-$(COMMON_VOICE_VERS)-$(COMMON_VOICE_LANG).tar.gz
corpus_dir          = cv-corpus-$(COMMON_VOICE_VERS)/$(COMMON_VOICE_LANG)
corpus_db           = $(corpus_dir).db
mfa                 = $(shell command -v mfa)
pythonpath          = $(abspath ..)
python              = PYTHONPATH=$(pythonpath) python -m
vocab_dirs          = $(foreach word,$(VOCAB),$(corpus_dir)/$(word))

.PHONY: help
help:
	@echo "make $(corpus_archive):\n  download the common voice corpus archive\n"
	@echo "make $(corpus_db):\n  create the courpus databse\n"
	@echo "make $(extract_vocab):\n  extract clips of target vocab ($(VOCAB))\n"

$(corpus_archive):
	$(python) magic_packet.datasets.cv_corpus.download_archive \
		. \
		--lang=$(COMMON_VOICE_LANG) \
		--version=$(COMMON_VOICE_VERS)

$(corpus_dir):
	mkdir -p $(corpus_dir)

$(corpus_db): $(corpus_dir)
	$(python) magic_packet.datasets.cv_corpus.database.create_database \
		./$(corpus_archive) \
		./$(corpus_db) \
		--overwrite \
		--splits train dev test

$(acoustic_model):
	mfa model download acoustic $(MFA_ACOUSTIC_MODEL)

.PHONY: extract_vocab
extract_vocab: $(corpus_db) lexicon.txt $(acoustic_model)
	$(python) magic_packet.datasets.cv_corpus.vocab.extract_vocab \
		./$(corpus_archive) \
		./$(corpus_db) \
		lexicon.txt \
		$(MFA_ACOUSTIC_MODEL) \
		./$(corpus_dir) \
		./$(corpus_dir) \
		--vocab $(VOCAB)

# $(corpus_dir)/alignments: N_JOBS ?= 8
# $(corpus_dir)/alignments: $(corpus_dir) lexicon.txt
# 	yes n | $(mfa) align --num_jobs $(N_JOBS) \
# 		$(corpus_dir)/clips \
# 		lexicon.txt \
# 		english \
# 		$@

lexicon.txt:
	curl $(LEXICON_URL) -o $@
