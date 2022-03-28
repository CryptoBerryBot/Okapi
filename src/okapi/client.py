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
