COMMON_VOICE_DIR   = "cv-corpus-7.0-2021-07-21/en"
DATA_DIR           = $(abspath ./data)
VOCAB              = '["fire"]'
INFERENCE_SEQUENCE = [0]

.PHONY: generate_raw_audio_dataset help

generate_raw_audio_dataset:
	./bin/howl/howl \
		-e VOCAB=$(VOCAB) \
		-e INFERENCE_SEQUENCE=$(INFERENCE_SEQUENCE) \
		-v $(DATA_DIR):/opt/data \
		-- generate_raw_audio_dataset \
		-i /opt/data/$(COMMON_VOICE_DIR) \
		-o /opt/data/raw_audio_dataset \
		--positive-pct 100 \
		--negative-pct 5

help:
	@echo "make generate_raw_audio_dataset  : generate raw audio dataset with howl"
