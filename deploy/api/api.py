import contextlib
import datetime
import os
import shutil
import sys
from typing import List

import librosa
import numpy as np
import soundfile
from fastapi import FastAPI, WebSocket, status
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


api = FastAPI()
settings = APISettings()
sys.path.insert(0, settings.multilingual_kws_path)


@api.post("/infer")
def infer():
    return status.HTTP_200_OK


@api.post("/reset")
def reset():
    with contextlib.suppress(FileNotFoundError):
        os.remove(settings.model_history_path)
    with contextlib.suppress(FileNotFoundError):
        os.remove(settings.model_path)
    shutil.rmtree(settings.samples_path, ignore_errors=True)
    os.mkdir(settings.samples_path)
    return status.HTTP_200_OK


@api.post("/sample")
def sample(sample: AudioSample):
    write_wav(sample)
    return status.HTTP_200_OK


@api.websocket("/train")
async def train(websocket: WebSocket):
    await websocket.accept()
    await websocket.send()
    try:
        history = model_train(
            settings.background_noise_path,
            settings.embedding_path,
            settings.samples_path,
            settings.model_path,
            settings.unknown_files_path,
        )
        await websocket.send_json(history)
        await websocket.close()
    except Exception as e:
        print(e)


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
