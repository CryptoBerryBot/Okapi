"""Kraken public API."""
from typing import Iterable

import httpx
from typeguard import typechecked

from ..client import Client


@typechecked
class PublicAPI:
    """Kraken public API."""

    def __init__(self, client: Client) -> None:
        self.api = "public"
        self.client = client

    def time(self) -> httpx.Response:
        """Get the server's time."""
        return self.client.post(url=self.client._url("Time"))

    def ohlc(
        self,
        *,
        pair: Iterable[str] = ("XBT", "USD"),
        interval: int = 1,
        since: int | None = None,
    ) -> httpx.Response:
        """Get OHLC Data."""
        data = {
            "pair": "".join(pair),
            "interval": interval,
        }

        if since is not None:
            data["since"] = since

        return self.client.post(
            url=self.client._url("OHLC"),
            data=data,
        )
