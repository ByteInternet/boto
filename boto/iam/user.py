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


class User(object):
    """
    Represents an IAM User
    """

    def __init__(self, connection=None, name=None):
        self.connection  = connection
        self.name        = name
        self.arn         = None
        self.create_date = None
        self.id          = None
        self.path        = None

    def __repr__(self):
        return 'User:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Arn':
            self.arn = value
        elif name == 'Path':
            self.path = value
        elif name == 'UserId':
            self.id = value
        elif name == 'UserName':
            self.name = value
        elif name == 'CreateDate':
            self.create_date = value
        else:
            setattr(self, name, value)


    def modify(self, new_user_name=None, new_path=None):
        """
        Updates the name and/or the path of the user.

        :type new_user_name: string
        :param new_user_name: If provided, the name of the user will be
            changed to this name.

        :type new_path: string
        :param new_path: If provided, the path of the certificate will be
            changed to this path.
        """
        rs = self.connection.update_user(self.name,
            new_user_name, new_path)

        if rs:
            if new_user_name:
                self.name = new_user_name
            if new_path:
                self.path = new_path

        return rs
