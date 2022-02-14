from typing import List

from fastapi import APIRouter
from pydantic import BaseModel


class AudioSample(BaseModel):
    data: List[int]
    sampleRate: int


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.post("/train")
async def train(sample: AudioSample) -> dict:
    return sample
