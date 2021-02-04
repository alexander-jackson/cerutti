# Cerutti

Cerutti is a client-server model for hosting auctions for the CS404 Agent Based
Systems coursework between students, without the need to share code.

## Getting Started

The server-side is currently hosted (sometimes) at `abs.blackboards.pl` and
waits to accept connections. To begin as a client, simply clone the repository,
install the requirements using `pip3 install -r requirements.txt` and copy your
code into `client/uXXXXXXX.py`.

You can then run `./client/main.py` to connect to the server, which should
inform you of the number of bots currently waiting for the auction.
