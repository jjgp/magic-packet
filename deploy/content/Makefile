.PHONY: all
all: multilingual_embedding multilingual_kws speech_commands unknown_files

.PHONY: help
help:
	@echo "make multilingual_embedding:\n    download multilingual embedding model\n"
	@echo "make multilingual_kws:\n    download multilingual kws source\n"
	@echo "make speech_commands:\n    download speech commands\n"
	@echo "make unknown_files:\n    download unknown files\n"

multilingual_embedding:
	@curl -LO \
		https://github.com/harvard-edge/multilingual_kws/releases/download/v0.1-alpha/multilingual_context_73_0.8011.tar.gz \
		&& tar -xzf multilingual_context_73_0.8011.tar.gz \
		&& mv multilingual_context_73_0.8011 multilingual_embedding

multilingual_kws:
	@curl -L \
		https://github.com/harvard-edge/multilingual_kws/tarball/main \
		| tar xz \
		&& mv harvard-edge-multilingual_kws-* multilingual_kws

speech_commands:
	@curl -LO \
		http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz \
		&& mkdir speech_commands \
		&& tar -xzf speech_commands_v0.02.tar.gz -C speech_commands

unknown_files:
	@curl -LO \
		https://github.com/harvard-edge/multilingual_kws/releases/download/v0.1-alpha/unknown_files.tar.gz \
		&& mkdir unknown_files \
		&& tar -xzf unknown_files.tar.gz -C unknown_files
