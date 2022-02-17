import contextlib
import datetime
import json
import os
import shutil
import sys
from typing import List

import librosa
import numpy as np
import soundfile
from fastapi import APIRouter, BackgroundTasks, status
from pydantic import BaseModel, BaseSettings

from .model import train as model_train


class AudioSample(BaseModel):
    data: List[int]
    rate: int


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
    def model_history_path(self):
        return os.path.join(self.content_dir, "model_history.json")

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


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)
settings = APISettings()
sys.path.insert(0, settings.multilingual_kws_path)


@router.post("/infer")
def infer():
    return status.HTTP_200_OK


@router.get("/poll")
def poll() -> dict:
    has_model = os.path.exists(settings.model_path)
    num_samples = len(os.listdir(settings.samples_path))
    model_history = {}
    if os.path.exists(settings.model_history_path):
        with open(settings.model_history_path, "r") as fobj:
            model_history = json.load(fobj)
    return dict(
        has_model=has_model, model_history=model_history, num_samples=num_samples
    )


@router.post("/reset")
def reset():
    setup()
    return status.HTTP_200_OK


@router.post("/sample")
def sample(sample: AudioSample):
    write_wav(sample)
    return status.HTTP_200_OK


def setup():
    with contextlib.suppress(FileNotFoundError):
        os.remove(settings.model_history_path)
    with contextlib.suppress(FileNotFoundError):
        os.remove(settings.model_path)
    shutil.rmtree(settings.samples_path, ignore_errors=True)
    os.mkdir(settings.samples_path)


@router.post("/train")
async def train(background_tasks: BackgroundTasks):
    background_tasks.add_task(
        model_train,
        settings.background_noise_path,
        settings.embedding_path,
        settings.model_history_path,
        settings.samples_path,
        settings.model_path,
        settings.unknown_files_path,
    )
    return status.HTTP_200_OK


def write_wav(sample: AudioSample):
    audio = np.array(sample.data, dtype=np.float32).reshape((len(sample.data),))
    resampled = librosa.resample(
        audio,
        orig_sr=sample.rate,
        target_sr=settings.rate_out,
        res_type="kaiser_fast",
        fix=True,
    )
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file = f"{settings.samples_path}/{now}.wav"
    soundfile.write(file, resampled, settings.rate_out, "PCM_16")
