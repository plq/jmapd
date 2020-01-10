
#
# This file is part of the jmapd project at https://github.com/arskom/jmapd.
#
# jmapd (c) 2020 and beyond, Arskom Ltd. All rights reserved.
#
# This file is subject to the terms of the 3-clause BSD license, which can be
# found in the LICENSE file distributed with this file. Alternatively, you can
# obtain a copy from the repository root cited above.
#


from neurons import Application
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.util import memoize

from jmapd.service.core import CoreReaderServices
from jmapd.service.mail import MailWriterServices, MailReaderServices


@memoize  # this makes sure the app is initialized only once
def start_core(config):
    subconfig = config.services['core']

    if subconfig.subapps is None:
        subconfig.subapps = {}

    subconfig.subapps.update({
        '': Application(
            [CoreReaderServices],
            tns='https://jmap.io/', name='CoreServices',
            in_protocol=HttpRpc(validator='soft'),
            out_protocol=JsonDocument(),
            config=config,
        ),
        'api': Application(
            [
                MailReaderServices, MailWriterServices,
            ],
            tns='https://jmap.io/', name='ApiServices',
            in_protocol=JsonDocument(validator='soft'),
            out_protocol=JsonDocument(),
            config=config,
        )
    })

    return subconfig.gen_site()
