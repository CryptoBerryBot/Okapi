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
"""Authentication for the Kraken API."""
import base64
import hashlib
import hmac
import urllib.parse
from dataclasses import dataclass
from typing import Generator

import httpx
from typeguard import typechecked


@typechecked
def _nonce_from_request(request: httpx.Request) -> bytes:
    data = urllib.parse.parse_qs(request.content.decode())
    nonce = data.get("nonce")
    if nonce is None:
        return bytes()

    return nonce[0].encode()


@typechecked
@dataclass
class KrakenAuth(httpx.Auth):
    """HTTPX Authentication class for the Kraken REST API."""

    key: str | None = None
    secret: str | None = None

    def sign_request(self, request: httpx.Request) -> str:
        """Give the signature for a request

        references:
            * https://docs.kraken.com/rest/
        """
        if self.key is None or self.secret is None:
            return ""

        nonce = _nonce_from_request(request)
        if len(nonce) == 0:
            return ""

        message = (
            request.url.raw_path
            + hashlib.sha256(nonce + request.content).digest()
        )

        mac = hmac.new(base64.b64decode(self.secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())

        return sigdigest.decode()

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        if self.key is not None and self.secret is not None:
            request.headers["API-Key"] = self.key
            request.headers["API-Sign"] = self.sign_request(request)

        yield request
