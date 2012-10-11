# Copyright (c) 2010 Mitch Garnaat http://garnaat.org/
# Copyright (c) 2010, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

class HostedZone(object):

    def __init__(self, id=None, name=None, owner=None, version=None,
                 caller_reference=None, resource_recordset_count=None):
        self.id = id
        self.name = name
        self.owner = owner
        self.version = version
        self.caller_reference = caller_reference
        self.resource_recordset_count = resource_recordset_count
        self.config = None
        self.change_info = None
        self.delegation_set = None

    def startElement(self, name, attrs, connection):
        if name == 'Config':
            self.config = Config(self)
            return self.config
        elif name == 'ChangeInfo':
            self.change_info = ChangeInfo(self)
            return self.change_info
        elif name == 'DelegationSet':
            self.delegation_set = DelegationSet(self)
            return self.delegation_set
        else:
            return None

    def endElement(self, name, value, connection):
        if name == 'Id':
            self.id = value.split('/')[2]
        elif name == 'Name':
            self.name = value
        elif name == 'Owner':
            self.owner = value
        elif name == 'Version':
            self.version = value
        elif name == 'CallerReference':
            self.caller_reference = value
        elif name == 'ResourceRecordSetCount':
            self.resource_recordset_count = value
        else:
            setattr(self, name, value)

class Config(object):

    def __init__(self, parent=None):
        self.parent = parent
        self.comment = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Comment':
            self.comment = value
        else:
            setattr(self, name, value)

class ChangeInfo(object):

    def __init__(self, parent=None):
        self.parent = parent
        self.id = None
        self.status = None
        self.submitted_at = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Id':
            self.id = value.split('/')[2]
        elif name == 'Status':
            self.status = value
        elif name == 'SubmittedAt':
            self.submitted_at = value
        else:
            setattr(self, name, value)

class DelegationSet(object):

    def __init__(self, parent=None):
        self.parent = parent
        self.name_servers = []

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'NameServer':
            self.name_servers.append(value)
        else:
            setattr(self, name, value)

