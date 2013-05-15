# Galah API Client

[Galah](/galah-group/galah) exposes an interface that a client application can
access. While anyone could make a compliant API client, this repo will contain
the official API client maintained alongside Galah.

## How to Install

Go to this [webpage](http://galah-group.github.com/galah-apiclient/) to find
links to downloads and documentation.

## License

The Galah API Client is licensed separately from Galah. It is licensed under
the Apache License v2 (see the LICENSE file).

## Design Philosophy

The API Client is at its core a script, and though it is spread out into
multiple files it retains the feeling of a script. Most functions do not throw
exceptions on failure, rather they log a critical failure and then call
`sys.exit(1)`.
