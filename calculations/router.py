from fastapi import APIRouter

from shemas.model import CoilHe

router = APIRouter(
    prefix="/calculations",
    tags=["Calculating"]
)


@router.get("/")
def calculation(coilHe: CoilHe):

    res = coilHe
    return {"data": res.geometry}
