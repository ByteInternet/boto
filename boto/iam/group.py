# Copyright (c) 2012 Gertjan Oude Lohuis, Byte Internet http://byte.nl/
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

from boto.resultset import ResultSet
from boto.iam.user import User


class Group(object):
    """
    Represents an IAM Group
    """

    def __init__(self, connection=None, name=None, endpoints=None):
        self.connection  = connection
        self.name        = name
        self.arn         = None
        self.id          = None
        self.path        = None
        self.users       = None

    def __repr__(self):
        return 'Group:%s' % self.name

    def startElement(self, name, attrs, connection):
        if name == 'Users':
            self.users = ResultSet([('member', User)])
            return self.users
        else:
            return None

    def endElement(self, name, value, connection):
        if name == 'Arn':
            self.arn = value
        elif name == 'Path':
            self.path = value
        elif name == 'GroupId':
            self.id = value
        elif name == 'GroupName':
            self.name = value
        else:
            setattr(self, name, value)

    def modify(self, new_group_name=None, new_path=None):
        """
        Updates the name and/or the path of the group.

        :type new_group_name: string
        :param new_group_name: If provided, the name of the group will be
            changed to this name.

        :type new_path: string
        :param new_path: If provided, the path of the certificate will be
            changed to this path.
        """
        rs = self.connection.update_group(self.name,
            new_group_name, new_path)

        if rs:
            if new_group_name:
                self.name = new_group_name
            if new_path:
                self.path = new_path

        return rs

    def add_user(self, user):
        """
        Add a user to the group

        :type :class:`boto.iam.user.User`
        :param user: instance of :class:`boto.iam.user.User` to add to the group
        """
        if not isinstance(user, User):
            raise Exception, "user must be an instance of boto.iam.user.User"

        rs = self.connection.add_user_to_group(self.name,
                user.name)

        # TODO: test
        if rs:
            self.users.append(user)

        return rs

    def remove_user(self, user):
        """
        Remove a user from the group

        :type :class:`boto.iam.user.User`
        :param user: instance of :class:`boto.iam.user.User` to remove from the group
        """
        if not isinstance(user, User):
            raise Exception, "user must be an instance of boto.iam.user.User"

        rs = self.connection.remove_user_from_group(self.name,
                user.name)

        # TODO: test
        # TODO: what happens if user does not exist
        if rs:
            self.users.remove(user)

        return rs




