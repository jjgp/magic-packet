import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="client/build", html=True), name="client")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
