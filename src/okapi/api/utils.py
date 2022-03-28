"""Utility functions for the Kraken API."""
import time

KrakenData = dict[str, int | bool | str]


def nonce() -> str:
    """Return a nounce counter (monotonic clock)."""
    return str(int(1000 * time.time()))


def nonce_data(data: KrakenData | None = None) -> KrakenData:
    """Add the nounce data to existing data."""
    if data is None:
        data = {}

    return {"nonce": nonce(), **data}
