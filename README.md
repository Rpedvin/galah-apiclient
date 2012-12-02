# Galah API Client

[Galah](/brownhead/galah) exposes an interface that a client application can
access. While anyone could make a compliant API client, this repo will contain
the official API client maintained alongside Galah.

## How to Install

Go to the [Downloads](/brownhead/galah/downloads) section and download the most
recent release tarbell. Unpack the archive wherever you'd like and execute the
file `api_client.py` normally. You do not need any elevated permissions to do
this.

If you'd like, you can add a symlink in one of the directories in your path
(such as `/usr/local/bin`) so you can execute the API client from any working
directory.

```shell
$ ln -s /usr/local/bin/api_client.py GALAH/API/ROOT/api_client.py
```

## License

The Galah API Client is licensed separately from Galah. It is "licensed" under
[The Unlicense](http://www.unlicense.org). All documentation for the API client
has also been placed under The Unlicense.

In short, feel free to use the code and documentation in this repository for any
purpose without restriction (though keep in mind this definitely does not apply
to the main Galah repository).

Also, feel free to create your own version of the API Client! If you do, I'd
gladly put a link up in this repo.