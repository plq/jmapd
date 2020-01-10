
#
# This file is part of the jmapd project at https://github.com/arskom/jmapd.
#
# jmapd (c) 2020 and beyond, Arskom Ltd. All rights reserved.
#
# This file is subject to the terms of the 3-clause BSD license, which can be
# found in the LICENSE file distributed with this file. Alternatively, you can
# obtain a copy from the repository root cited above.
#

import logging
logger = logging.getLogger(__name__)

from pprint import pformat

from spyne import rpc

from jmapd.model import Capabilities
from jmapd.service import ReaderBase


class CoreReaderServices(ReaderBase):
    @rpc(_returns=Capabilities.customize(wrapper='capabilities'))
    def jmap(ctx):
        retval = Capabilities(
            core=ctx.app.config.caps_core,
            mail=ctx.app.config.caps_mail,
        )

        logger.info("%s", pformat(retval))

        return retval
