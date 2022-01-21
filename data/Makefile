COMMON_VOICE_LANG ?= en
COMMON_VOICE_VERS ?= 7.0-2021-07-21
LEXICON_URL       ?= https://www.openslr.org/resources/11/librispeech-lexicon.txt

corpus_archive     = cv-corpus-$(COMMON_VOICE_VERS)-$(COMMON_VOICE_LANG).tar.gz
corpus_dir         = cv-corpus-$(COMMON_VOICE_VERS)/$(COMMON_VOICE_LANG)
pythonpath         = $(abspath ..)
python             = PYTHONPATH=$(pythonpath) python -m

.PHONY: help
help:
	@echo "make $(corpus_archive):\n  download the common voice corpus archive\n"
	@echo "make $(corpus_dir):\n  extract the common voice corpus from the archive\n"
	@echo "make lexicon.txt:\n  download the lexicon\n"

$(corpus_archive):
	$(python) magic_packet.datasets.cv_corpus.download \
		$(abspath .) \
		--lang=$(COMMON_VOICE_LANG) \
		--version=$(COMMON_VOICE_VERS)

$(corpus_dir):
	tar -xzf $(corpus_archive)

lexicon.txt:
	curl $(LEXICON_URL) -o $@
