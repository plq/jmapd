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

import pytz

from datetime import datetime

from spyne import M, ComplexModel, UnsignedInteger, AnyDict, Unicode, Array, \
    DateTime, SelfReference, Boolean

from jmapd.model import UtcDate, JmapId


class EmailHeader(ComplexModel):
    _type_info = [
        ('key', M(Unicode(default=''))),
        # sub_name used just to be consistent with EmailAddressGroup
        ('value', M(Unicode(default='', sub_name='email'))),
    ]


class EmailAddress(ComplexModel):
    _type_info = [
        ('name', M(Unicode(default=''))),
        # sub_name used just to be consistent with EmailAddressGroup
        ('address', M(Unicode(default='', sub_name='email'))),
    ]

    def is_empty(self):
        return (self.name is None and self.address is None) \
                             or (len(self.name) == 0 and len(self.address) == 0)


class EmailAddressGroup(ComplexModel):
    _type_info = [
        ('name', M(Unicode(default=''))),
        ('addresses', Array(M(Unicode(default='')))),
    ]


class EmailBodyValue(ComplexModel):
    _type_info = [
        ('value', Unicode(
            doc='String The value of the body part after decoding '
                'Content-Transfer-Encoding and the Content-Type charset, '
                'if both known to the server, and with any CRLF replaced with '
                'a single LF. The server MAY use heuristics to determine the '
                'charset to use for decoding if the charset is unknown, '
                'no charset is given, or it believes the charset given is '
                'incorrect. Decoding is best effort; the server SHOULD insert '
                'the unicode replacement character (U+FFFD) and continue when '
                'a malformed section is encountered.\n\n'

                'Note that due to the charset decoding and line ending '
                'normalisation, the length of this string will probably not '
                'be exactly the same as the size property on the '
                'corresponding EmailBodyPart.'
        )),

        ('is_encoding_problem', M(Boolean(
            sub_name='isEncodingProblem', default=False,
            doc='Boolean (default: false) This is true if malformed sections '
                'were found while decoding the charset, or the charset was '
                'unknown, or the content-transfer-encoding was unknown.',
        ))),

        ('is_truncated', M(Boolean(
            sub_name='isTruncated', default=False,
            doc='Boolean (default: false) This is true if the value has been '
                'truncated.',
        ))),
    ]


class EmailBodyPart(ComplexModel):
    _type_info = [
        ('part_id', Unicode(
            sub_name='partId',
            doc='String|null Identifies this part uniquely within the Email. '
                'This is scoped to the emailId and has no meaning outside of '
                'the JMAP Email object representation. This is null if, '
                'and only if, the part is of type multipart/*.'
        )),

        ('blob_id', JmapId(
            sub_name='blobId',
            doc='Id|null The id representing the raw octets of the contents '
                'of the part, after decoding any known '
                'Content-Transfer-Encoding (as defined in [@!RFC2045]), '
                'or null if, and only if, the part is of type multipart/*. '
                'Note that two parts may be transfer-encoded differently but '
                'have the same blob id if their decoded octets are identical '
                'and the server is using a secure hash of the data for the '
                'blob id. If the transfer encoding is unknown, it is treated '
                'as though it had no transfer encoding.'
        )),

        ('size', M(UnsignedInteger(
            sub_name='size',
            doc='UnsignedInt The size, in octets, of the raw data after '
                'content transfer decoding (as referenced by the blobId, '
                'i.e., the number of octets in the file the user would '
                'download).'
        ))),

        ('headers', Array(EmailHeader,
            sub_name='headers',
            doc='EmailHeader[] This is a list of all header fields in the '
                'part, in the order they appear in the message. The values '
                'are in Raw form.'
        )),

        ('name', Unicode(
            sub_name='name',
            doc='String|null This is the decoded filename parameter of the '
                'Content-Disposition header field per [@!RFC2231], or (for '
                'compatibility with existing systems) if not present, '
                'then it’s the decoded name parameter of the Content-Type '
                'header field per [@!RFC2047].'
        )),

        ('type', M(Unicode(
            sub_name='type',
            doc='String The value of the Content-Type header field of the '
                'part, if present; otherwise, the implicit type as per the '
                'MIME standard (text/plain or message/rfc822 if inside a '
                'multipart/digest). CFWS is removed and any parameters are '
                'stripped.'
        ))),

        ('charset', Unicode(
            sub_name='charset',
            doc='String|null The value of the charset parameter of the '
                'Content-Type header field, if present, or null if the header '
                'field is present but not of type text/*. If there is no '
                'Content-Type header field, or it exists and is of type '
                'text/* but has no charset parameter, this is the implicit '
                'charset as per the MIME standard: us-ascii.'
        )),

        ('disposition', Unicode(
            sub_name='disposition',
            doc='String|null The value of the Content-Disposition header '
                'field of the part, if present; otherwise, it’s null. CFWS is '
                'removed and any parameters are stripped.'
        )),

        ('cid', Unicode(
            sub_name='cid',
            doc='String|null The value of the Content-Id header field of the '
                'part, if present; otherwise it’s null. CFWS and surrounding '
                'angle brackets (<>) are removed. This may be used to '
                'reference the content from within a text/html body part HTML '
                'using the cid: protocol, as defined in [@!RFC2392].'
        )),

        ('language', Array(Unicode,
            sub_name='language',
            doc='String[]|null The list of language tags, as defined in ['
                '@!RFC3282], in the Content-Language header field of the '
                'part, if present.'
        )),

        ('location', Unicode(
            sub_name='location',
            doc='String|null The URI, as defined in [@!RFC2557], in the '
                'Content-Location header field of the part, if present.'
        )),

        ('subParts', Array(SelfReference,
            sub_name='subParts',
            doc='EmailBodyPart[]|null If the type is multipart/*, '
                'this contains the body parts of each child.'
        )),
    ]


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

        ('mailbox_ids', AnyDict(  # this is supposed to be a JmapId: bool dict
            sub_name='mailboxIds',
            doc="The set of Mailbox ids this Email belongs to. An "
                "Email in the mail store MUST belong to one or more Mailboxes "
                "at all times (until it is destroyed). The set is represented "
                "as an object, with each key being a Mailbox id. The value "
                "for each key in the object MUST be true."
        )),

        ('keywords', AnyDict(  # this is supposed to be a str: bool dict
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
            default_factory=lambda: datetime.utcnow().replace(tzinfo=pytz.utc)
                                                                   .isoformat(),
            sub_name='receivedAt',
            doc="(immutable; default: time of creation on server) The "
                "date the Email was received by the message store. This is "
                "the internal date in IMAP [@?RFC3501]."
        )),

        #
        # Header fields
        #

        ('message_id', Array(Unicode,
            sub_name='messageId',
            doc='String[]|null (immutable) The value is identical to the '
                'value of header:Message-ID:asMessageIds. For messages '
                'conforming to RFC 5322 this will be an array with a single '
                'entry.'
        )),

        ('in_reply_to', Array(Unicode,
            sub_name='inReplyTo',
            doc='String[]|null (immutable) The value is identical to the '
                'value of header:In-Reply-To:asMessageIds.'
        )),

        ('references', Array(Unicode,
            sub_name='references',
            doc='String[]|null (immutable) The value is identical to the '
                'value of header:References:asMessageIds.'
        )),

        ('sender', Array(EmailAddress,
            sub_name='sender',
            doc='EmailAddress[]|null (immutable) The value is identical to '
                'the value of header:Sender:asAddresses.'
        )),

        ('from_', Array(Unicode,
            sub_name='from',
            doc='EmailAddress[]|null (immutable) The value is identical to '
                'the value of header:From:asAddresses.'
        )),

        ('to', Array(Unicode,
            sub_name='to',
            doc='EmailAddress[]|null (immutable) The value is identical to '
                'the value of header:To:asAddresses.'
        )),

        ('cc', Array(Unicode,
            sub_name='cc',
            doc='EmailAddress[]|null (immutable) The value is identical to '
                'the value of header:Cc:asAddresses.'
        )),

        ('bcc', Array(Unicode,
            sub_name='bcc',
            doc='EmailAddress[]|null (immutable) The value is identical to '
                'the value of header:Bcc:asAddresses.'
        )),

        ('reply_to', Unicode(
            sub_name='replyTo',
            doc='EmailAddress[]|null (immutable) The value is identical to '
                'the value of header:Reply-To:asAddresses.'
        )),

        ('subject', Unicode(
            sub_name='subject',
            doc='String|null (immutable) The value is identical to the value '
                'of header:Subject:asText.'
        )),

        ('sent_at', DateTime(
            sub_name='sentAt',
            doc='Date|null (immutable; default on creation: current server '
                'time) The value is identical to the value of '
                'header:Date:asDate.'
        )),

        #
        # Body Parts
        #

        ('body_structure', Array(EmailBodyPart,
            sub_name='bodyStructure',
            doc='EmailBodyPart (immutable) This is the full MIME structure of '
                'the message body, without recursing into message/rfc822 or '
                'message/global parts. Note that EmailBodyParts may have '
                'subParts if they are of type multipart/*.'
        )),

        ('body_values', AnyDict(
            sub_name='bodyValues',
            doc='String[EmailBodyValue] (immutable) This is a map of partId '
                'to an EmailBodyValue object for none, some, or all text/* '
                'parts. Which parts are included and whether the value is '
                'truncated is determined by various arguments to Email/get '
                'and Email/parse.'
        )),

        ('text_body', Array(EmailBodyPart,
            sub_name='textBody',
            doc='EmailBodyPart[] (immutable) A list of text/plain, text/html, '
                'image/*, audio/*, and/or video/* parts to display ('
                'sequentially) as the message body, with a preference for '
                'text/plain when alternative versions are available.'
        )),

        ('html_body', Array(EmailBodyPart,
            sub_name='htmlBody',
            doc='EmailBodyPart[] (immutable) A list of text/plain, text/html, '
                'image/*, audio/*, and/or video/* parts to display ('
                'sequentially) as the message body, with a preference for '
                'text/html when alternative versions are available.'
        )),

        ('attachments', Array(EmailBodyPart,
            sub_name='attachments',
            doc='EmailBodyPart[] (immutable) A list, traversing depth-first, '
                'of all parts in bodyStructure that satisfy either of the '
                'following conditions:'
        )),

        ('has_attachment', M(Boolean(
            sub_name='hasAttachment', default=False,
            doc='Boolean (immutable; server-set) This is true if there are '
                'one or more parts in the message that a client UI should '
                'offer as downloadable. A server SHOULD set hasAttachment to '
                'true if the attachments list contains at least one item that '
                'does not have Content-Disposition: inline. The server MAY '
                'ignore parts in this list that are processed automatically '
                'in some way or are referenced as embedded images in one of '
                'the text/html parts of the message.'
        ))),

        ('preview', Unicode(256,
            sub_name='preview', default=u'',
            doc='String (immutable; server-set) A plaintext fragment of the '
                'message body. This is intended to be shown as a preview line '
                'when listing messages in the mail store and may be truncated '
                'when shown. The server may choose which part of the message '
                'to include in the preview; skipping quoted sections and '
                'salutations and collapsing white space can result in a more '
                'useful preview.'
        )),
    ]
