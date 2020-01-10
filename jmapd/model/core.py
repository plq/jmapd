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

from __future__ import unicode_literals

from spyne import M, ComplexModel, Unicode, UnsignedInteger, Array, Boolean
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


class MailCapabilities(ComplexModel):
    _type_info = [
        ('max_mailboxes_per_email', UnsignedInteger(
            sub_name='maxMailboxesPerEmail',
            doc="The maximum number of Mailboxes (see "
                "Section 2) that can be can assigned to a single Email "
                "object (see Section 4). This MUST be an integer >= 1, "
                "or null for no limit (or rather, the limit is always the "
                "number of Mailboxes in the account)."
        )),

        ('max_mailbox_depth', UnsignedInteger(
            sub_name='maxMailboxDepth',
            doc="The maximum depth of the Mailbox hierarchy "
                "(i.e., one more than the maximum number of ancestors a "
                "Mailbox may have), or null for no limit."
        )),

        ('max_size_mailbox_name', M(UnsignedInteger(
            sub_name='maxSizeMailboxName',
            doc="The maximum length, in (UTF-8) octets, allowed "
                "for the name of a Mailbox. This MUST be at least 100, "
                "although it is recommended servers allow more."
        ))),

        ('max_size_attachments_per_email', M(UnsignedInteger(
            sub_name='maxSizeAttachmentsPerEmail',
            doc="The maximum total size of attachments, "
                "in octets, allowed for a single Email object. A server MAY "
                "still reject the import or creation of an Email with a "
                "lower attachment size total (for example, if the body "
                "includes several megabytes of text, causing the size of the "
                "encoded MIME structure to be over some server-defined "
                "limit).\n\n"

                "Note that this limit is for the sum of unencoded attachment "
                "sizes. Users are generally not knowledgeable about encoding "
                "overhead, etc., nor should they need to be, so marketing "
                "and help materials normally tell them the “max size "
                "attachments”. This is the unencoded size they see on their "
                "hard drive, so this capability matches that and allows the "
                "client to consistently enforce what the user understands as "
                "the limit.\n\n"

                "The server may separately have a limit for the total size "
                "of the message [@!RFC5322], created by combining the "
                "attachments (often base64 encoded) with the message headers "
                "and bodies. For example, suppose the server advertises "
                "maxSizeAttachmentsPerEmail: 50000000 (50 MB). The enforced "
                "server limit may be for a message size of 70000000 octets. "
                "Even with base64 encoding and a 2 MB HTML body, "
                "50 MB attachments would fit under this limit."
        ))),

        ('email_query_sort_options', Array(Unicode,
            sub_name='emailQuerySortOptions',
            doc="A list of all the values the server supports for "
                "the “property” field of the Comparator object in an "
                "Email/query sort (see Section 4.4.2). This MAY include "
                "properties the client does not recognise (for example, "
                "custom properties specified in a vendor extension). Clients "
                "MUST ignore any unknown properties in the list."
        )),

        ('may_create_top_level_mailbox', Boolean(
             sub_name='mayCreateTopLevelMailbox',
             doc="If true, the user may create a Mailbox (see Section "
                 "2) in this account with a null parentId. (Permission for "
                 "creating a child of an existing Mailbox is given by the "
                 "myRights property on that Mailbox.)"
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
        ('mail', MailCapabilities.customize(
            # standard sub_name value is invalid XML so it's restricted to
            # dict-based protocols.
            pa={DictDocument: dict(sub_name='urn:ietf:params:jmap:mail')}
        )),
    ]
