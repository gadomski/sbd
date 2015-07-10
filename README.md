sbd
===

Python daemon and library for receiving and parsing Iridium Short Burst Data (SBD) messages.
Known to work on Python 2.6 and 2.7 with only [one dependency](https://pypi.python.org/pypi/python-daemon/).


Installation
------------

```bash
pip install git+https://github.com/gadomski/sbd@master
```


Using the daemon
----------------

The provided daemon, `iridiumd`, will run in the background and receive DirectIP messages from the Iridium service.
Run `iridiumd -h` to see the command line options.

The daemon will receive and parse incoming Iridium messages and store them in a directory hierarchy specified at daemon initialization.
The daemon does not require any sort of special permissions and can run as any user.
Messages are stored as follows: `<IMEI number>/<year>/<month>/<timestamp>.{sbd|payload}`, where:

- `<IMEI number>` is the IMEI number of the sending modem
- `<year>`, `<month>`, `<timestamp>` are all from the timestamp contained in the Iridium message itself
- Files ending in `.sbd` are the entire Iridium message, including headers
- Files ending in `.payload` are the Iridium message payload, stripped of headers

There are a few houskeeping files in the top level of the working directory; their names should be relatively self-explanatory.
Monitor `server.log` for information about incoming messages and any problems that arise during message parsing.


Using the library
-----------------

You can use the `sbd` library to parse Iridium messages, including those stored on the filesystem by the daemon.
The parsing capabilities are not complete and are relatively undocumented, so you'll want to read through the tests or the source to get an idea of how to use things.


Licence
-------

This software is under the MIT license.
