# jmapd

A Pure-python server implementation for JMAP (https://jmap.io).

https://github.com/arskom/jmapd

To get started:

    $ virtualenv venv
    $ source venv/bin/activate
    $ python setup.py develop

To run the daemon:

    $ source venv/bin/activate
    $ jmapd

You can use ``jmapd --autoreload`` to have code changes reflect instantly.

The server listens on TCP4:localhost:8100 by default. You may need to start it
twice to let it generate a config file first.

Once the server is up and running, run:

    $ curl localhost:8100/jmap | python3 -m json.tool

to get the capabilities object.
