from fastapi import APIRouter

from .. import repository
from ..models import ProfileIn, ProfileOut

router = APIRouter()


@router.get("/profile", response_model=ProfileOut)
def read_profile():
    return repository.get_profile()


@router.put("/profile", response_model=ProfileOut)
def update_profile(profile: ProfileIn):
    return repository.upsert_profile(profile.model_dump())
