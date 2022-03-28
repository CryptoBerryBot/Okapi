"""Kraken HTTPX Client."""
from typing import Any

import httpx
from typeguard import typechecked

from . import __version__
from .auth import KrakenAuth


HTTPXClientKwargs = Any


@typechecked
class Client(httpx.Client):
    """HTTX based Kraken client."""

    def __init__(
        self,
        *,
        key: str | None = None,
        secret: str | None = None,
        name: str = f"okapi/{__version__}",
        domain: str = "https://api.kraken.com",
        api: str = "public",
        api_version: int = 0,
        **kwargs: HTTPXClientKwargs,
    ) -> None:
        super().__init__(
            base_url=f"{domain}/{api_version}",
            auth=KrakenAuth(key=key, secret=secret),
            headers={"User-Agent": name},
            **kwargs,
        )
        self.api = api

    def url(self, method: str) -> str:
        """Return the URL for a given method."""
        return f"{self.api}/{method}"
