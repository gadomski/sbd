import struct


class Message(object):
    """An Iridium SBD message."""

    @classmethod
    def read(cls, filename):
        """Reads an sbd message stored on the filesystem and returns the Message."""
        with open(filename, "rb") as f:
            return Message.parse(f.read())

    @classmethod
    def parse(cls, string):
        message = cls()
        message.protocol_revision_number, message.overall_message_length = struct.unpack("!bH", string[0:3])
        index = 3
        while index < message.overall_message_length:
            information_element, offset = InformationElement.parse(string[index:])
            message.add_information_element(information_element)
            index += offset
        return message

    def __init__(self):
        self._protocol_revision_number = None
        self._overall_message_length = None
        self._information_elements = []

    @property
    def protocol_revision_number(self):
        return self._protocol_revision_number

    @protocol_revision_number.setter
    def protocol_revision_number(self, value):
        self._protocol_revision_number = value

    @property
    def overall_message_length(self):
        return self._overall_message_length 

    @overall_message_length.setter
    def overall_message_length(self, value):
        self._overall_message_length = value

    def add_information_element(self, information_element):
        self._information_elements.append(information_element)


class InformationElement(object):
    """An Iridium message Information Element."""

    @classmethod
    def parse(cls, string):
        information_element = cls() 
        information_element.id_, information_element.length = struct.unpack("!bH", string[0:3])
        offset = information_element.length + 3
        information_element.data = string[3:offset]
        return information_element, offset

    def __init__(self):
        self._id = None
        self._length = None

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, value):
        self._id = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value
