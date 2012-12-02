# Galah API Client

[Galah](/brownhead/galah) exposes an interface that a client application can
access. While anyone could make a compliant API client, this repo will contain
the official API client maintained alongside Galah.

## How to Install

You can use `pip` to install the API client, however, this may not be an option
available to you if you don't have root privileges on your system, so you may
also download a self-contained tarbell. Instructions for doing both are included
below.

### Installing with pip

This is by far the easiest installation method. If you already have `pip`
installed (which is a package manager for Python prjoects), just run

```shell
$ pip install galah-apiclient
```

If you don't have pip, [you'll have to install it first](https://www.google.com/search?q=python+how+to+get+pip).

### Installing from tarbell

Go to the [Downloads](/brownhead/galah/downloads) section and download the most
recent release tarbell. Unpack the archive wherever you'd like and execute the
file `api_client.py` normally. You do not need any elevated permissions to do
this.

## License

The Galah API Client is licensed separately from Galah. It is "licensed" under
[The Unlicense](http://www.unlicense.org). All documentation for the API client
has also been placed under The Unlicense.