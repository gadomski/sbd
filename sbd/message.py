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

    def get_information_element(self, index):
        return self._information_elements[index]


class InformationElement(object):
    """An Iridium message Information Element."""

    @staticmethod
    def parse(string):
        id_, length = struct.unpack("!bH", string[0:3])
        if id_ == 1:
            cls = MobileOriginatedHeader
        elif id_ == 2:
            cls = MobileOriginatedPayload
        elif id_ == 3:
            cls = MobileOriginatedLocationInformation
        elif id_ == 41:
            cls = MobileTerminatedHeader
        elif id_ == 42:
            cls = MobileTerminatedPayload
        elif id_ == 44:
            cls = MobileTerminatedConfirmationMessage
        information_element = cls(id_, length)
        offset = 3 + length
        information_element.read(string[4:offset])
        return information_element, offset

    def __init__(self, id_, length):
        self._id = id_
        self._length = length

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

    def read(self, string):
        raise NotImplemented


class MobileOriginatedHeader(InformationElement):
    
    def __init__(self, id_, length):
        super(MobileOriginatedHeader, self).__init__(id_, length)
        self._cdr_reference = None

    def read(self, string):
        print struct.unpack(string[0:2], "!b")
        self.cdr_reference, self.imei, self.session_status, self.momsn, \
                self.mtmsn, self.time_of_session = struct.unpack(string, "!bHI15sBHHI")

    @property
    def cdr_reference(self):
        return self._cdr_reference

    @cdr_reference.setter
    def cdr_reference(self, value):
        self._cdr_reference = value


class MobileOriginatedPayload(InformationElement):

    def read(self, string):
        None
