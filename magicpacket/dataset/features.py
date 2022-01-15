import tensorflow as tf


def mfcc(
    y=None,
    sr=16000,
    S=None,
    n_mfcc=13,
    n_fft=255,
    hop_length=128,
    fmin=80.0,
    fmax=7600.0,
    n_mels=128,
):
    """
    https://www.tensorflow.org/api_docs/python/tf/signal/mfccs_from_log_mel_spectrograms
    """

    S = S if S is not None else spectrogram(y, sr, n_fft, hop_length)

    # Warp the linear scale spectrograms into the mel-scale.
    num_spectrogram_bins = S.shape[-1]
    linear_to_mel_weight_matrix = tf.signal.linear_to_mel_weight_matrix(
        n_mels, num_spectrogram_bins, sr, fmin, fmax
    )
    mel_spectrogram = tf.tensordot(S, linear_to_mel_weight_matrix, 1)
    mel_spectrogram.set_shape(
        S.shape[:-1].concatenate(linear_to_mel_weight_matrix.shape[-1:])
    )

    # Compute a stabilized log to get log-magnitude mel-scale spectrograms.
    log_mel_spectrogram = tf.math.log(mel_spectrogram + 1e-6)
    # Compute MFCCs from log_mel_spectrograms and take the first 13.
    return tf.signal.mfccs_from_log_mel_spectrograms(log_mel_spectrogram)[..., :n_mfcc]


def normalize(y):
    return tf.cast(y, dtype=tf.float32) / 32768.0


def spectrogram(y, n_samples=16000, n_fft=255, hop_length=128):
    """
    https://www.tensorflow.org/tutorials/audio/simple_audio#convert_waveforms_to_spectrograms
    """

    y = y[:n_samples]
    padded = zero_padding(y, n_samples)
    # Convert the waveform to a spectrogram via a STFT.
    stft = tf.signal.stft(
        padded, frame_length=n_fft, frame_step=hop_length, fft_length=n_fft
    )
    # Obtain the magnitude of the STFT.
    return tf.abs(stft)


def zero_padding(y, n_samples):
    zero_padding = tf.zeros([n_samples] - tf.shape(y), dtype=tf.float32)
    y = tf.cast(y, dtype=tf.float32)
    # Concatenate the waveform with `zero_padding`, which ensures all audio
    # clips are of the same length.
    return tf.concat([y, zero_padding], 0)
