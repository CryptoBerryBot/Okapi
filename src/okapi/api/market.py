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
from datetime import datetime
from typing import Any
from typing import Iterable

import httpx
import numpy as np
import pandas as pd
from typeguard import typechecked

from ..client import Client
from .utils import content
from .utils import public_url

Pair = list[tuple[str, str]] | tuple[str, str] | list[str] | str


@typechecked
def _make_array(junk: Any) -> np.ndarray:
    return np.asarray(junk).astype(np.float)


@typechecked
def _make_pair(pair: Pair) -> str:
    if isinstance(pair, list):
        pair = ",".join(pair)

    if isinstance(pair, tuple):
        pair = "".join(pair)

    return pair


@typechecked
def _format_ohlc(
    ohlc: pd.DataFrame, *, interval: int, ascending: bool = True
) -> pd.DataFrame:
    if ohlc.empty:
        return ohlc

    ohlc["dtime"] = pd.to_datetime(ohlc.time, unit="s")
    ohlc.sort_values("dtime", ascending=ascending, inplace=True)
    ohlc.set_index("dtime", inplace=True)
    freq = str(interval) + "T" if ascending else str(-interval) + "T"
    ohlc.index.freq = freq
    for col in ["open", "high", "low", "close", "vwap", "volume"]:
        ohlc.loc[:, col] = ohlc[col].astype(float)

    return ohlc


@typechecked
class MarketRESTAPI:
    """Kraken public API."""

    valid_interval = (1, 5, 15, 30, 60, 240, 1440, 10080, 21600)
    info = ("info", "leverage", "fees", "margin")

    def __init__(self, client: Client) -> None:
        self.client = client

    def server_time(
        self,
        *,
        raw: bool = False,
    ) -> httpx.Response | dict[str, datetime | int]:
        """Get the server's time."""
        response = self.client.get(url=public_url("Time"))
        if raw:
            return response

        response = content(response)
        response["unixtime"] = int(response["unixtime"])
        response["rfc1123"] = datetime.strptime(
            response["rfc1123"],
            "%a, %d %b %y %H:%M:%S %z",
        )
        return response

    def system_status(
        self,
        *,
        raw: bool = False,
    ) -> httpx.Response | dict[str, datetime | int]:
        """Get the current system status or trading mode."""
        response = self.client.get(url=public_url("SystemStatus"))
        if raw:
            return response

        response = content(response)
        response["timestamp"] = datetime.strptime(
            response["timestamp"],
            "%Y-%m-%dT%H:%M:%SZ",
        )
        return response

    def asset_info(
        self,
        asset: Iterable[str] | str = "XBT",
        *,
        aclass: str = "currency",
        raw: bool = False,
    ) -> httpx.Response | pd.DataFrame:
        """Get information about the assets that are available for deposit,
        withdrawal, trading and staking."""
        if isinstance(asset, str):
            asset = (asset,)

        response = self.client.get(
            url=public_url("Assets"),
            params={
                "asset": ",".join(asset),
                "aclass": aclass,
            },
        )
        if raw:
            return response

        response = content(response)
        return pd.DataFrame(response)

    def tradable_asset_pairs(
        self,
        pair: Pair = ("XBT", "USD"),
        *,
        info: str = "info",
        raw: bool = False,
    ) -> httpx.Response | pd.DataFrame:
        """Get tradable asset pairs."""
        if info not in self.info:
            raise ValueError(f"{info} not invalid info {self.info}")

        pair = _make_pair(pair)

        data = {
            "pair": "".join(pair),
            "info": info,
        }

        response = self.client.get(
            url=public_url("AssetPairs"),
            params=data,
        )
        if raw:
            return response

        response = content(response)
        response = pd.DataFrame.from_dict(
            response,
            orient="index",
        )
        response = response.astype(
            dtype={
                "pair_decimals": "int",
                "lot_decimals": "int",
                "lot_multiplier": "int",
                "margin_call": "int",
                "margin_stop": "int",
                "ordermin": "float",
            }
        )
        response["fees"] = response["fees"].map(_make_array)
        response["fees_maker"] = response["fees_maker"].map(_make_array)
        response["leverage_buy"] = response["leverage_buy"].map(_make_array)
        response["leverage_sell"] = response["leverage_sell"].map(_make_array)
        return response

    def ticker_information(
        self,
        pair: Pair = ("XBT", "USD"),
        *,
        raw: bool = False,
    ) -> httpx.Response | pd.DataFrame:
        """Get Ticker Information.

        Note: Today's prices start at midnight UTC
        """
        pair = _make_pair(pair)

        data = {
            "pair": "".join(pair),
        }

        response = self.client.get(
            url=public_url("Ticker"),
            params=data,
        )
        if raw:
            return response

        response = content(response)
        response = pd.DataFrame.from_dict(
            response,
            orient="index",
        )
        response["a"] = response["a"].map(_make_array)
        response["b"] = response["b"].map(_make_array)
        response["c"] = response["c"].map(_make_array)
        response["v"] = response["v"].map(_make_array)
        response["p"] = response["p"].map(_make_array)
        response["t"] = response["t"].map(_make_array)
        response["l"] = response["h"].map(_make_array)
        response["h"] = response["l"].map(_make_array)
        response["o"] = response["o"].map(_make_array)
        return response

    def ohlc_data(
        self,
        pair: Pair = ("XBT", "USD"),
        *,
        interval: int = 1,
        since: int | None = None,
        raw: bool = False,
    ) -> httpx.Response | dict[str, pd.DataFrame | int]:
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

        response = self.client.get(
            url=public_url("OHLC"),
            params=data,
        )
        if raw:
            return response

        response = content(response)
        last = int(response.pop("last"))
        response = {
            pair: _format_ohlc(
                pd.DataFrame(
                    ohlc,
                    columns=[
                        "time",
                        "open",
                        "high",
                        "low",
                        "close",
                        "vwap",
                        "volume",
                        "count",
                    ],
                ),
                interval=interval,
            )
            for pair, ohlc in response.items()
        }
        response["last"] = last
        return response
