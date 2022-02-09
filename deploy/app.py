from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/client", StaticFiles(directory="client/build", html=True), name="client")


@app.get("/")
async def root():
    return RedirectResponse(url="/client")
