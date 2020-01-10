
#
# This file is part of the jmapd project at https://github.com/arskom/jmapd.
#
# jmapd (c) 2020 and beyond, Arskom Ltd. All rights reserved.
#
# This file is subject to the terms of the 3-clause BSD license, which can be
# found in the LICENSE file distributed with this file. Alternatively, you can
# obtain a copy from the repository root cited above.
#

from __future__ import unicode_literals

from datetime import datetime

from spyne import ComplexModel, M, DateTime, Any, Integer64, IpAddress


class LogEntry(ComplexModel):
    _type_info = [
        ('id', M(Integer64(pk=True))),
        ('time', M(DateTime(
            timezone=False, default_factory=lambda: datetime.utcnow(),
        ))),
        ('host', IpAddress),
        ('data', Any),
    ]
