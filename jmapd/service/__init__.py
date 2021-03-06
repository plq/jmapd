
#
# This file is part of the jmapd project at https://github.com/arskom/jmapd.
#
# jmapd (c) 2020 and beyond, Arskom Ltd. All rights reserved.
#
# This file is subject to the terms of the 3-clause BSD license, which can be
# found in the LICENSE file distributed with this file. Alternatively, you can
# obtain a copy from the repository root cited above.
#

from neurons.base.service import TReaderService, TWriterService

from jmapd.model import LogEntry

ReaderBase = TReaderService(LogEntry)
WriterBase = TWriterService(LogEntry)
