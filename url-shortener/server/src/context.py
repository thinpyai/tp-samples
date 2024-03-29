"""
Context module.
This module provide contexts of the system.

Returns:
    UrlContext: Url context which can access to url services.
"""
from fastapi import Depends
from strawberry.fastapi import BaseContext

from database import get_db
from domain.service.url_service import UrlService
from infra.repository.url_repository import UrlRepository


class UrlContext(BaseContext):
    """UrlContext BaseContext

    Args:
        BaseContext (BaseContext): FastAPI router base Context
    """

    def __init__(self, url_service: UrlService):
        """
        Initialize URL service to UrlContext

        Args:
            url_service (UrlService): URL service
        """
        self.url_service: UrlService = url_service


def get_url_repository(db=Depends(get_db)) -> UrlRepository:
    """
    Get URL repository

    Args:
        db (SessionLocal, optional): Database session. Defaults to Depends(get_db).

    Returns:
        UrlRepository: URL Tepository
    """
    return UrlRepository(db)


def get_url_service(url_repository: UrlRepository = Depends(get_url_repository)):
    """Get url service class object.

    Returns:
        UrlService: UrlService class object
    """
    return UrlService(url_repository=url_repository)


async def get_url_context(
        url_service: UrlService = Depends(get_url_service)) -> UrlContext:
    """Get UrlContext class object.

    Args:
        url_service (UrlService, optional): UrlService class object. Defaults to Depends(get_url_service).

    Returns:
        UrlContext: UrlContext class object
    """
    return UrlContext(url_service=url_service)
