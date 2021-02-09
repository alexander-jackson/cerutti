import argparse

from cerutti import client
from cerutti import server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--client", action="store_true", help="Run the module as a client"
    )
    group.add_argument(
        "--server", action="store_true", help="Run the module as a server"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.client:
        client.start()
    else:
        server.start()
