#
# This file is part of the jmapd project at https://github.com/arskom/jmapd.
#
# jmapd (c) 2020 and beyond, Arskom Ltd. All rights reserved.
#
# This file is subject to the terms of the 3-clause BSD license, which can be
# found in the LICENSE file distributed with this file. Alternatively, you can
# obtain a copy from the repository root cited above.
#

import sys

from neurons.daemon import main
from neurons.daemon import ServiceDaemon, ServiceDefinition, HttpServer

from jmapd.model.core import CoreCapabilities, MailCapabilities


class JmapDaemon(ServiceDaemon):
    caps_core = CoreCapabilities
    caps_mail = MailCapabilities

    @classmethod
    def get_default(cls, daemon_name):
        retval = super(JmapDaemon, cls).get_default(daemon_name)

        # no database needed yet.
        del retval.stores['sql_main']

        retval.caps_core = CoreCapabilities(
            max_size_upload=50 * 1024 * 1024,
            max_concurrent_upload=4,
            max_size_request=100 * 1024 * 1024,
            max_concurrent_requests=4,
            max_calls_in_request=32,
            max_objects_in_get=50,
            max_objects_in_set=20,
            collation_algorithms=[
                'C',
            ],
        )

        return retval


def init_jmapd(config):
    from jmapd.app import start_core

    return [
        ('core', ServiceDefinition(
            init=start_core,
            default=HttpServer(
                type='tcp4', host='127.0.0.1', port=8100,
            )
        )),
    ]


def jmapd_main():
    return main('jmapd', sys.argv, init_jmapd, cls=JmapDaemon)
