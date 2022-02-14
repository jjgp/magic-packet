from typing import List

from fastapi import APIRouter, status
from pydantic import BaseModel


class AudioSample(BaseModel):
    data: List[int]
    sampleRate: int


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.post("/infer")
async def infer(sample: AudioSample) -> dict:
    return sample


@router.post("/reset")
async def reset() -> dict:
    return status.HTTP_200_OK


@router.get("/poll")
async def poll() -> dict:
    return status.HTTP_200_OK


@router.post("/train")
async def train(sample: AudioSample) -> dict:
    return sample
