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

from spyne import ComplexModel, UnsignedInteger, AnyDict

from jmapd.model import UtcDate, JmapId

r"""
Keywords are shared with IMAP. The six system keywords from IMAP get special
treatment. The following four keywords have their first character changed
from \ in IMAP to $ in JMAP and have particular semantic meaning:

    $draft: The Email is a draft the user is composing.
    $seen: The Email has been read.
    $flagged: The Email has been flagged for urgent/special attention.
    $answered: The Email has been replied to.

The IMAP \Recent keyword is not exposed via JMAP. The IMAP \Deleted keyword
is also not present: IMAP uses a delete+expunge model, which JMAP does not.
Any message with the \Deleted keyword MUST NOT be visible via JMAP (and so
are not counted in the “totalEmails”, “unreadEmails”, “totalThreads”,
and “unreadThreads” Mailbox properties).

Users may add arbitrary keywords to an Email. For compatibility with IMAP,
a keyword is a case-insensitive string of 1–255 characters in the ASCII
subset %x21–%x7e (excludes control chars and space), and it MUST NOT include
any of these characters:

  ( ) { ] % * " \

Because JSON is case sensitive, servers MUST return keywords in lowercase.

The IMAP and JMAP Keywords registry as established in [@!RFC5788] assigns
semantic meaning to some other keywords in common use. New keywords may be
established here in the future. In particular, note:

    $forwarded: The Email has been forwarded.
    $phishing: The Email is highly likely to be phishing. Clients SHOULD warn
        users to take care when viewing this Email and disable links and
        attachments.
    $junk: The Email is definitely spam. Clients SHOULD set this flag when
        users report spam to help train automated spam-detection systems.
    $notjunk: The Email is definitely not spam. Clients SHOULD set this flag
        when users indicate an Email is legitimate, to help train automated
        spam-detection systems.

"""


class Email(ComplexModel):
    _type_info = [
        #
        # Metadata
        #

        ('id', JmapId(
            sub_name='id',
            doc="Id (immutable; server-set) The id of the Email object. Note "
                "that this is the JMAP object id, NOT the Message-ID header "
                "field value of the message [@!RFC5322]."
        )),

        ('blob_id', JmapId(
            sub_name='blobId',
            doc="Id (immutable; server-set) The id representing the raw "
                "octets of the message [@!RFC5322] for this Email. This may "
                "be used to download the raw original message or to attach it "
                "directly to another Email, etc."
        )),

        ('thread_id', JmapId(
            sub_name='threadId',
            doc="(immutable; server-set) The id of the Thread to which "
                "this Email belongs."
        )),

        ('mailbox_ids', AnyDict(  # this is supposed to be a JmapId: Boolean dict
            sub_name='mailboxIds',
            doc="The set of Mailbox ids this Email belongs to. An "
                "Email in the mail store MUST belong to one or more Mailboxes "
                "at all times (until it is destroyed). The set is represented "
                "as an object, with each key being a Mailbox id. The value "
                "for each key in the object MUST be true."
        )),

        ('keywords', AnyDict(  # this is supposed to be a String: Boolean dict
            sub_name='keywords',
            doc="(default: {}) A set of keywords that apply "
                "to the Email. The set is represented as an object, with the "
                "keys being the keywords. The value for each key in the "
                "object MUST be true."
        )),

        ('size', UnsignedInteger(
            sub_name='size',
            doc="(immutable; server-set) The size, in octets, "
                "of the raw data for the message [@!RFC5322] (as referenced "
                "by the blobId, i.e., the number of octets in the file the "
                "user would download)."
        )),

        ('received_at', UtcDate(
            sub_name='receivedAt',
            doc="(immutable; default: time of creation on server) The "
                "date the Email was received by the message store. This is "
                "the internal date in IMAP [@?RFC3501]."
        )),
    ]
