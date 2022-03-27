"""Authentication for the Kraken API."""
import base64
import hashlib
import hmac
import urllib.parse
from dataclasses import dataclass
from typing import Generator
from typing import Optional

import httpx
from typeguard import typechecked


def _nonce_from_request(request: httpx.Request) -> str:
    data = urllib.parse.parse_qs(request.content.decode())
    return data["nonce"][0].encode()


@typechecked
@dataclass
class KrakenAuth(httpx.Auth):
    """HTTPX Authentication class for the Kraken REST API."""

    key: Optional[str] = None
    secret: Optional[str] = None

    def sign_request(self, request: httpx.Request) -> str:
        """Give the signature for a request

        reference: https://docs.kraken.com/rest/
        """
        nonce = _nonce_from_request(request)
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
