from fastapi import APIRouter

from .. import repository
from ..models import Article

router = APIRouter()


@router.get("/articles", response_model=list[Article])
def list_articles(category: str | None = None):
    return repository.list_articles(category)
