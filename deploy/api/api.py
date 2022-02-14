from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.post("/train")
async def train() -> dict:
    return {"message": "hello from api"}
