import datetime
import os
import shutil
from typing import List

import librosa
import numpy as np
import soundfile
from fastapi import APIRouter, BackgroundTasks, status
from pydantic import BaseModel, BaseSettings


class AudioSample(BaseModel):
    data: List[int]
    rate: int


class APISettings(BaseSettings):
    content_dir: str = os.path.abspath("./content")
    rate_out: int = 16000

    @property
    def model_path(self):
        return os.path.join(self.content_dir, "model.h5")

    @property
    def samples_dir(self):
        return os.path.join(self.content_dir, "samples")


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)
settings = APISettings()


@router.post("/infer")
def infer(sample: AudioSample) -> dict:
    return sample


@router.get("/poll")
def poll() -> dict:
    has_model = os.path.exists(settings.model_path)
    num_samples = len(os.listdir(settings.samples_dir))
    return dict(has_model=has_model, num_samples=num_samples)


@router.post("/reset")
def reset() -> dict:
    setup()
    return status.HTTP_200_OK


@router.post("/sample")
async def sample(sample: AudioSample, background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(write_wav, sample)
    return status.HTTP_200_OK


def setup():
    shutil.rmtree(settings.samples_dir, ignore_errors=True)
    os.mkdir(settings.samples_dir)


@router.on_event("startup")
def startup():
    setup()


@router.post("/train")
async def train(background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(train_model)
    return status.HTTP_200_OK


def train_model():
    pass


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
    file = f"{settings.samples_dir}/{now}.wav"
    soundfile.write(file, resampled, settings.rate_out, "PCM_16")
