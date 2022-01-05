COMMON_VOICE_DIR           ?= cv-corpus-7.0-2021-07-21/en
LEXICON_URL                ?= https://www.openslr.org/resources/11/librispeech-lexicon.txt
NUM_JOBS                   ?= 8
VOCAB                      ?= fire

inference_sequence          = $(shell seq -s, 0 $(shell grep -o '_' <<<$(1) | grep -c .) | sed s'/,$$//')
raw_dir                     = ./raw
vocab_dir                   = $(raw_dir)/$(VOCAB)
negative_aligned_metadata   = $(addprefix $(vocab_dir)/negative/aligned-metadata-,$(addsuffix .jsonl,dev test training))
positive_dir     	        = $(vocab_dir)/positive
positive_aligned_metadata   = $(addprefix $(positive_dir)/aligned-metadata-,$(addsuffix .jsonl,dev test training))
positive_alignment_dir      = $(positive_dir)/alignment
positive_stitched_dir       = $(positive_dir)/stitched
vocab_sequence              = $(shell sed 's/_/","/g' <<<$(1))
howl                        = cd $(abspath ../howl) \
    && VOCAB='["$(call vocab_sequence,$(VOCAB))"]' INFERENCE_SEQUENCE='[$(call inference_sequence,$(VOCAB))]'

.PHONY : all
all: $(positive_stitched_dir) $(negative_aligned_metadata)

.PHONY: help
help:
	@echo "make $(vocab_dir):\n  Create positive ($(call vocab_sequence,$(VOCAB))) and negative samples/metadata\n"
	@echo "make lexicon.txt:\n  Download the lexicon\n"
	@echo "make $(positive_alignment_dir):\n  Create aligned metadata files\n"
	@echo "make $(positive_aligned_metadata):\n  mfa align positive samples\n"
	@echo "make $(positive_stitched_dir):\n  Stitch aligned positive samples\n"
	@echo "make $(negative_aligned_metadata):\n  Stub the alignment of the negative samples"

$(vocab_dir): $(COMMON_VOICE_DIR)
	@($(howl) python -m training.run.generate_raw_audio_dataset \
		-i $(COMMON_VOICE_DIR) \
		-o $(raw_dir) \
		--positive-pct 100 \
		--negative-pct 5)

lexicon.txt:
	curl $(LEXICON_URL) -o $@

$(positive_alignment_dir): $(vocab_dir) lexicon.txt
	yes n | mfa align --num_jobs $(NUM_JOBS) \
		$(positive_dir)/audio \
		lexicon.txt \
		english \
		$(positive_alignment_dir)

$(positive_aligned_metadata): $(positive_alignment_dir)
	@($(howl) python -m training.run.attach_alignment \
		--input-raw-audio-dataset $(positive_dir) \
  		--token-type word \
  		--alignment-type mfa \
  		--alignments-path $(positive_alignment_dir))

$(positive_stitched_dir): $(positive_aligned_metadata)
	@($(howl) python -m training.run.stitch_vocab_samples \
		--aligned-dataset $(positive_dir) \
		--stitched-dataset $(positive_stitched_dir))

$(negative_aligned_metadata): $(vocab_dir)
	@($(howl) python -m training.run.attach_alignment \
		--alignment-type stub \
		--input-raw-audio-dataset $(vocab_abspath)/negative \
		--token-type word)
