"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Okapi."""


if __name__ == "__main__":
    main()  # pragma: no cover
