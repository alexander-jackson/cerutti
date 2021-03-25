import argparse

from cerutti import client
from cerutti import server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(help="Subcommands for running a client or server")

    client_parser = subparser.add_parser("client", help="Client arguments")
    client_parser.add_argument(
        "--base",
        type=str,
        default="abs.blackboards.pl",
        help="The base URL of the server",
    )
    client_parser.add_argument(
        "--port", type=int, default=8765, help="The port to connect to"
    )
    client_parser.add_argument(
        "--gametype",
        type=str,
        choices=["value", "collection"],
        required=True,
        help="The gametype to play against other bots",
    )
    client_parser.add_argument(
        "--bots",
        type=int,
        required=True,
        help="The number of bots to play against",
    )
    client_parser.set_defaults(func=client.start)

    server_parser = subparser.add_parser("server", help="Client arguments")
    server_parser.add_argument("--port", type=int, default=8765)
    server_parser.set_defaults(func=server.start)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    args.func(args)
