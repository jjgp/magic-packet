COMMON_VOICE_LANG ?= en
COMMON_VOICE_VERS ?= 7.0-2021-07-21
LEXICON_URL       ?= https://www.openslr.org/resources/11/librispeech-lexicon.txt
# VOCAB             ?= hey fire fox

corpus_archive     = cv-corpus-$(COMMON_VOICE_VERS)-$(COMMON_VOICE_LANG).tar.gz
corpus_dir         = cv-corpus-$(COMMON_VOICE_VERS)/$(COMMON_VOICE_LANG)
corpus_db          = $(corpus_dir).db
conda_run_mfa      = conda run --no-capture-output -n mfa mfa
mfa                = $(if $(shell command -v mfa),mfa,$(conda_run_mfa))
pythonpath         = $(abspath ..)
python             = PYTHONPATH=$(pythonpath) python -m

.PHONY: help
help:
	@echo "make $(corpus_archive):\n  download the common voice corpus archive\n"
	@echo "make $(corpus_dir):\n  extract the common voice corpus from the archive\n"
	@echo "make $(corpus_dir)/alignments:\n  align the audio files\n"
	@echo "make lexicon.txt:\n  download the lexicon\n"

$(corpus_archive):
	$(python) magic_packet.datasets.cv_corpus.download \
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
