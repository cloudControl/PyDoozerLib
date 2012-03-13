# PyDoozerLib

A Python client for [Doozer](https://github.com/ha/doozerd).

## Latest version

The latest is `0.1.1`.

## Installation

Install via `pip`:

	$ pip install git+ssh://git@github.com/cloudControl/PyDoozerLib.git@0.1.1

### Installation error with protobuf 2.4.1

There is a case when you try to install `pydoozerlib` via `python setup.py install` and run into following error:

    [..]
    Downloading http://protobuf.googlecode.com/files/protobuf-2.4.1.zip
    Processing protobuf-2.4.1.zip
    error: Couldn't find a setup script in /tmp/easy_install-riZxUs/protobuf-2.4.1.zip

Simply install `protobuf` via `pip` manually:

    $ pip install protobuf

Then run `python setup.py install` again!

#### More information

Using the `pip install git+ssh://...` method doesn't seem to run into this issue.

For more information check following issue: [Protobuf Issue #66](http://code.google.com/p/protobuf/issues/detail?id=66)

## Usage

Using `PyDoozerLib` is dead simple.

Establish a connection to a running doozerd node:

	client = PyDoozerLib(doozerd_host, doozerd_port)
	client.connect()

Get the value at '/watch':

	print client.get('/watch').value

Overwrite the given value at '/watch' with a new value:

	client.set('/watch', 'Some random value to be set')

Delete a value:

	rev = client.get('/watch').rev
	client.delete('/watch', rev)

And disconnect:

	client.disconnect()

## Hacking on PyDoozerLib

Make sure to go through following points if you want to modify `PyDoozerLib`.

### Creating protobuf stub

In the `<project_root>/protobuf` directory you will find a `msg.proto` file. First, install `protobuf`, e.g. on Mac:

	$ brew install protobuf

Then, compile the proto file with `protoc`:

	$ protoc --python_output=. msg.proto

This will create a `msg_pb2.py` which can then be used in your Python project.

## Todo

 * tests
 * documentation

## Contributors

 * Hans-Gunther Schmidt <hgs@cloudcontrol.de>

## License

MIT