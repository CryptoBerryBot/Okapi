# Copyright 2022 Romain Brault
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Kraken public API."""
from typing import Iterable

import httpx
from typeguard import typechecked

from ..client import Client
from .utils import public_url

Pair = list[tuple[str, str]] | tuple[str, str] | list[str] | str


def _make_pair(pair: Pair) -> str:
    if isinstance(pair, list):
        pair = ",".join(pair)

    if isinstance(pair, tuple):
        pair = "".join(pair)

    return pair


@typechecked
class MarketRESTAPI:
    """Kraken public API."""

    valid_interval = (1, 5, 15, 30, 60, 240, 1440, 10080, 21600)
    info = ("info", "leverage", "fees", "margin")

    def __init__(self, client: Client) -> None:
        self.client = client

    def server_time(self) -> httpx.Response:
        """Get the server's time."""
        return self.client.get(url=public_url("Time"))

    def system_status(self) -> httpx.Response:
        """Get the current system status or trading mode."""
        return self.client.get(url=public_url("SystemStatus"))

    def asset_info(
        self, asset: Iterable[str] | str = "XBT", *, aclass: str = "currency"
    ) -> httpx.Response:
        """Get information about the assets that are available for deposit,
        withdrawal, trading and staking."""
        if isinstance(asset, str):
            asset = (asset,)

        return self.client.get(
            url=public_url("Assets"),
            params={
                "asset": ",".join(asset),
                "aclass": aclass,
            },
        )

    def tradable_asset_pairs(
        self,
        pair: Pair = ("XBT", "USD"),
        *,
        info: str = "info",
    ) -> httpx.Response:
        """Get tradable asset pairs."""
        if info not in self.info:
            raise ValueError(f"{info} not invalid info {self.info}")

        pair = _make_pair(pair)

        data = {
            "pair": "".join(pair),
            "info": info,
        }

        return self.client.get(
            url=public_url("AssetPairs"),
            params=data,
        )

    def ticker_information(
        self,
        pair: Pair = ("XBT", "USD"),
    ) -> httpx.Response:
        """Get Ticker Information.

        Note: Today's prices start at midnight UTC
        """
        pair = _make_pair(pair)

        data = {
            "pair": "".join(pair),
        }

        return self.client.get(
            url=public_url("Ticker"),
            params=data,
        )

    def ohlc_data(
        self,
        pair: Pair = ("XBT", "USD"),
        *,
        interval: int = 1,
        since: int | None = None,
    ) -> httpx.Response:
        """Get OHLC Data."""
        pair = _make_pair(pair)

        if interval not in self.valid_interval:
            raise ValueError(
                f"interval {interval} not in valid intervals "
                f"{self.valid_interval}."
            )

        data = {
            "pair": "".join(pair),
            "interval": interval,
        }

        if since is not None:
            data["since"] = since

        return self.client.get(
            url=public_url("OHLC"),
            params=data,
        )
