import contextlib
import datetime
import os
import shutil
import sys
from typing import List

import librosa
import numpy as np
import soundfile
from fastapi import APIRouter, status
from pydantic import BaseModel, BaseSettings

from .model import predict as model_predict
from .model import train as model_train


class APISettings(BaseSettings):
    content_dir: str = os.path.abspath("./content")
    rate_out: int = 16000

    @property
    def background_noise_path(self):
        return os.path.join(self.content_dir, "speech_commands/_background_noise_")

    @property
    def embedding_path(self):
        return os.path.join(self.content_dir, "multilingual_embedding")

    @property
    def model_path(self):
        return os.path.join(self.content_dir, "model.h5")

    @property
    def multilingual_kws_path(self):
        return os.path.join(self.content_dir, "multilingual_kws")

    @property
    def samples_path(self):
        return os.path.join(self.content_dir, "samples")

    @property
    def unknown_files_path(self):
        return os.path.join(self.content_dir, "unknown_files")


class AudioSample(BaseModel):
    data: List[float]
    rate: int


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)
settings = APISettings()
sys.path.insert(0, settings.multilingual_kws_path)


@router.post("/predict")
def predict(sample: AudioSample):
    resampled = resampled_audio(sample)
    prediction = model_predict(resampled, settings.model_path)
    return dict(prediction=np.squeeze(prediction).tolist())


def resampled_audio(sample):
    audio = np.array(sample.data, dtype=np.float32).reshape((len(sample.data),))
    resampled = librosa.resample(
        audio, orig_sr=sample.rate, target_sr=settings.rate_out, res_type="kaiser_fast"
    )
    return librosa.util.fix_length(resampled, size=settings.rate_out)


@router.post("/reset")
def reset():
    with contextlib.suppress(FileNotFoundError):
        os.remove(settings.model_path)
    shutil.rmtree(settings.samples_path, ignore_errors=True)
    os.mkdir(settings.samples_path)
    return status.HTTP_200_OK


@router.post("/sample")
def sample(sample: AudioSample):
    write_wav(sample)
    return status.HTTP_200_OK


@router.get("/train")
def train():
    return model_train(
        settings.background_noise_path,
        settings.embedding_path,
        settings.samples_path,
        settings.model_path,
        settings.unknown_files_path,
    )


def write_wav(sample: AudioSample):
    resampled = resampled_audio(sample)
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file = f"{settings.samples_path}/{now}.wav"
    soundfile.write(file, resampled, settings.rate_out, "PCM_16")
