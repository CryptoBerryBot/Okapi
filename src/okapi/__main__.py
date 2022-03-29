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
"""Command-line interface."""
import click
import pandas as pd
from typeguard import typechecked

from .api.kraken import KrakenRESTAPI
from .client import Client


@click.group()
@click.option("-k", "--key", type=str)
@click.option("-s", "--secret", type=str)
@click.version_option()
@click.pass_context
@typechecked
def main(ctx, key: str | None, secret: str | None) -> None:
    """Okapi."""
    ctx.obj = ctx.with_resource(Client(key=key, secret=secret))


@main.command()
@click.pass_obj
@typechecked
def server_time(client: Client) -> None:
    """Get the server's time."""
    kapi = KrakenRESTAPI(client)
    response = kapi.market.server_time()
    click.echo(response)


@main.command()
@click.pass_obj
@typechecked
def system_status(client: Client) -> None:
    """Get the current system status or trading mode."""
    kapi = KrakenRESTAPI(client)
    response = kapi.market.system_status()
    click.echo(response)


@main.command()
@click.option("-a", "--asset", type=str)
@click.option("--aclass", type=str, default="currency")
@click.pass_obj
@typechecked
def asset_info(client: Client, asset: str | None, aclass: str) -> None:
    """Get the current system status or trading mode."""
    kapi = KrakenRESTAPI(client)
    response = kapi.market.asset_info(asset=asset, aclass=aclass)
    click.echo(response)


@main.command()
@click.option("-p", "--pair", type=str, default="XBTUSD")
@click.option("--info", type=str, default="info")
@click.pass_obj
@typechecked
def tradable_asset_pairs(client: Client, pair: str, info: str) -> None:
    """Get the current system status or trading mode."""
    kapi = KrakenRESTAPI(client)
    response = kapi.market.tradable_asset_pairs(pair=pair, info=info)
    click.echo(response.T)


@main.command()
@click.option("-p", "--pair", type=str, default="XBTUSD")
@click.pass_obj
@typechecked
def ticker_information(client: Client, pair: str) -> None:
    """Get the current system status or trading mode."""
    kapi = KrakenRESTAPI(client)
    response = kapi.market.ticker_information(pair=pair)
    click.echo(response.T)


@main.command()
@click.option("-p", "--pair", type=str, default="XBTUSD")
@click.option("-i", "--interval", type=int, default=1)
@click.option("-s", "--since", type=int)
@click.pass_obj
@typechecked
def ohlc_data(
    client: Client, pair: str, interval: int, since: int | None
) -> None:
    """Get the current system status or trading mode."""
    kapi = KrakenRESTAPI(client)
    response = kapi.market.ohlc_data(pair=pair, interval=interval, since=since)
    last = response.pop("last")
    pd.set_option("display.max_rows", None)
    for current_pair, current_ohlc in response.items():
        click.echo(f"pair: {current_pair}")
        click.echo(current_ohlc)

    click.echo(f"last: {last}")


if __name__ == "__main__":
    main()  # type: ignore  # pragma: no cover  # pylint: disable=no-value-for-parameter,line-too-long
