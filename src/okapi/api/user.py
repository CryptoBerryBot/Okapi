"""Kraken User's Data private API."""
import httpx
from typeguard import typechecked

from ..client import Client
from .utils import nonce_data


@typechecked
class DataAPI:
    """Kraken User's data API."""

    def __init__(self, client: Client) -> None:
        self.client = client
        self.client.api = "private"

    def account_balance(self) -> httpx.Response:
        """Retrieve all cash balances, net of pending withdrawals."""
        return self.client.post(
            url=self.client.url("Balance"),
            data=nonce_data(),
        )

    def trade_balance(self, asset: str = "ZUSD") -> httpx.Response:
        """Retrieve all cash balances, net of pending withdrawals."""
        return self.client.post(
            url=self.client.url("TradeBalance"),
            data=nonce_data({"asset": asset}),
        )
