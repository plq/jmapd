# encoding: utf8
#
# This file is part of the jmapd project at https://github.com/arskom/jmapd.
#
# jmapd (c) 2020 and beyond, Arskom Ltd. All rights reserved.
#
# This file is subject to the terms of the 3-clause BSD license, which can be
# found in the LICENSE file distributed with this file. Alternatively, you can
# obtain a copy from the repository root cited above.
#


from spyne import ComplexModel, Unicode, UnsignedInteger, Array
from spyne.protocol.dictdoc import DictDocument


class CoreCapabilities(ComplexModel):
    _type_info = [
        ('max_size_upload', UnsignedInteger(
            subname='maxSizeUpload',
            doc="The maximum file size, in octets, that the server will "
                "accept for a single file upload (for any purpose). Suggested "
                "minimum: 50,000,000."
        )),
        ('max_concurrent_upload', UnsignedInteger(
            subname='maxConcurrentUpload',
            doc="The maximum number of concurrent requests the server will "
                "accept to the upload endpoint. Suggested minimum: 4."
        )),
        ('max_size_request', UnsignedInteger(
            subname='maxSizeRequest',
            doc="The maximum size, in octets, that the server will accept for "
                "a single request to the API endpoint. Suggested minimum: 10,"
                "000,000."
        )),
        ('max_concurrent_requests', UnsignedInteger(
            subname='maxConcurrentRequests',
            doc="The maximum number of concurrent requests the server will "
                "accept to the API endpoint. Suggested minimum: 4."
        )),
        ('max_calls_in_request', UnsignedInteger(
            subname='maxCallsInRequest',
            doc="The maximum number of method calls the server will accept in "
                "a single request to the API endpoint. Suggested minimum: 16."
        )),
        ('max_objects_in_get', UnsignedInteger(
            subname='maxObjectsInGet',
            doc="The maximum number of objects that the client may request in "
                "a single /get type method call. Suggested minimum: 500."
        )),
        ('max_objects_in_set', UnsignedInteger(
            subname='maxObjectsInSet',
            doc="The maximum number of objects the client may send to create, "
                "update, or destroy in a single /set type method call. This "
                "is the combined total, e.g., if the maximum is 10, you could "
                "not create 7 objects and destroy 6, as this would be 13 "
                "actions, which exceeds the limit. Suggested minimum: 500."
        )),
        ('collation_algorithms', Array(Unicode,
            subname='collationAlgorithms',
            doc="A list of identifiers for algorithms registered in the "
                "collation registry, as defined in [@!RFC4790], that the "
                "server supports for sorting when querying records."
        )),
    ]


class Capabilities(ComplexModel):
    """
    An object specifying the capabilities of this server. Each key is a URI for
    a capability supported by the server. The value for each of these keys is
    an object with further information about the server’s capabilities in
    relation to that capability.

    The client MUST ignore any properties it does not understand.
    """

    _type_info = [
        ('core', CoreCapabilities.customize(
            # standard sub_name value is invalid XML so it's restricted to
            # dict-based protocols.
            pa={DictDocument: dict(sub_name='urn:ietf:params:jmap:core')}
        )),
    ]
