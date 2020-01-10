
#
# This file is part of the jmapd project at https://github.com/arskom/jmapd.
#
# jmapd (c) 2020 and beyond, Arskom Ltd. All rights reserved.
#
# This file is subject to the terms of the 3-clause BSD license, which can be
# found in the LICENSE file distributed with this file. Alternatively, you can
# obtain a copy from the repository root cited above.
#

from spyne import M, Unicode, DateTime


UtcDate = DateTime(timezone=False)

#
# Quoting: https://jmap.io/spec-core.html#the-id-data-type
#
#     These characters are safe to use in almost any context (e.g., filesystems,
#     URIs, and IMAP atoms). For maximum safety, servers SHOULD also follow
#     defensive allocation strategies to avoid creating risks where glob
#     completion or data type detection may be present (e.g., on filesystems or
#     in spreadsheets). In particular, it is wise to avoid:
#
#      - Ids starting with a dash
#      - Ids starting with digits
#      - Ids that contain only digits
#      - Ids that differ only by ASCII case (for example, A vs. a)
#      - the specific sequence of three characters “NIL” (because this sequence
#      - can be confused with the IMAP protocol expression of the null value)
#
#     A good solution to these issues is to prefix every id with a single
#     alphabetical character.
#
# Hence the lowercase letter as the initial character
#

JmapId = M(Unicode(255, pattern='[a-z][A-Za-z0-9_-]+'))
