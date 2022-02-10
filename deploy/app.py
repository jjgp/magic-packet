from api import api
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/client", StaticFiles(directory="client/build", html=True), name="client")
app.include_router(api.router)


@app.get("/")
async def main():
    return RedirectResponse(url="/client")
