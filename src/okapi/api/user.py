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
"""Kraken User's Data private API."""
import httpx
from typeguard import typechecked

from ..client import Client
from .utils import nonce_data
from .utils import private_url


@typechecked
class DataRESTAPI:
    """Kraken User's data API."""

    def __init__(self, client: Client) -> None:
        self.client = client

    def account_balance(self) -> httpx.Response:
        """Retrieve all cash balances, net of pending withdrawals."""
        return self.client.post(
            url=private_url("Balance"),
            data=nonce_data(),
        )

    def trade_balance(self, asset: str = "ZUSD") -> httpx.Response:
        """Retrieve all cash balances, net of pending withdrawals."""
        return self.client.post(
            url=private_url("TradeBalance"),
            data=nonce_data({"asset": asset}),
        )
