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
"""Kraken REST API."""
from typeguard import typechecked

from ..client import Client
from .market import MarketRESTAPI
from .user import DataRESTAPI


@typechecked
class KrakenRESTAPI:  # pylint: disable=too-few-public-methods
    """Kraken REST API."""

    def __init__(self, client: Client) -> None:
        self.market = MarketRESTAPI(client)
        self.user = DataRESTAPI(client)
