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
"""Utility functions for the Kraken API."""
import time

import httpx
from typeguard import typechecked

from ..exception import KrakenAPIError


KrakenData = dict[str, int | bool | str]


@typechecked
def nonce() -> str:
    """Return a nounce counter (monotonic clock).

    References:
        * https://support.kraken.com/hc/en-us/articles/360000906023-What-is-a-nonce-
    """  # pylint: disable=line-too-long
    return str(time.monotonic_ns())


@typechecked
def nonce_data(data: KrakenData | None = None) -> KrakenData:
    """Add the nounce data to existing data."""
    if data is None:
        data = {}

    return {"nonce": nonce(), **data}


@typechecked
def public_url(method: str) -> str:
    """Return the private URL for a given method."""
    return f"public/{method}"


@typechecked
def private_url(method: str) -> str:
    """Return the private URL for a given method."""
    return f"private/{method}"


@typechecked
def content(response: httpx.Response) -> dict[str, str | list[str]]:
    """Check a response for error."""
    response.raise_for_status()
    json = response.json()
    if len(json["error"]) > 0:
        raise KrakenAPIError(json["error"])

    return json["result"]
