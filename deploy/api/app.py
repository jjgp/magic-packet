from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api", api.router)


@app.websocket("/foobar")
async def foobar(websocket):
    pass
