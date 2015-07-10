import struct


class Message(object):
    """An Iridium SBD message."""

    @classmethod
    def read(cls, filename):
        """Reads an sbd message stored on the filesystem and returns the Message."""
        with open(filename, "rb") as f:
            return cls.parse(f)

    @classmethod
    def parse(cls, stream):
        message = cls()
        message.protocol_revision_number, message.overall_message_length = struct.unpack("!bH", stream.read(3))
        while True:
            bytes_ = stream.read(3)
            if not bytes_:
                break
            id_, length = struct.unpack("!bH", bytes_)
            if id_ == 1:
                iecls = MobileOriginatedHeader
            elif id_ == 2:
                iecls = MobileOriginatedPayload
            elif id_ == 3:
                iecls = MobileOriginatedLocationInformation
            elif id_ == 41:
                iecls = MobileTerminatedHeader
            elif id_ == 42:
                iecls = MobileTerminatedPayload
            elif id_ == 44:
                iecls = MobileTerminatedConfirmationMessage
            else:
                raise InvalidInformationElementId(id_)
            message.add_information_element(iecls(id_, length, stream.read(length)))
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


class MobileOriginatedMessage(Message):

    @classmethod
    def parse(cls, stream):
        message = super(MobileOriginatedMessage, cls).parse(stream)
        header = message.get_information_element(0)
        message.time_of_session = header.time_of_session
        message.imei = header.imei
        message.payload = message.get_information_element(1).payload
        return message

    def __init__(self):
        super(MobileOriginatedMessage, self).__init__()
        self._time_of_session = None
        self._imei = None
        self._payload = None

    @property
    def time_of_session(self):
        return self._time_of_session

    @time_of_session.setter
    def time_of_session(self, value):
        self._time_of_session = value

    @property
    def imei(self):
        return self._imei

    @imei.setter
    def imei(self, value):
        self._imei = value

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value


class InformationElement(object):
    """An Iridium message Information Element."""

    def __init__(self, id_, length, data):
        self._id = id_
        self._length = length
        self._data = data

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


class MobileOriginatedHeader(InformationElement):
    
    def __init__(self, id_, length, data):
        super(MobileOriginatedHeader, self).__init__(id_, length, data)
        self._cdr_reference, self._imei, self._session_status, \
                self._momsn, self._mtmsn, self._time_of_session = struct.unpack("!I15sBHHI", data)

    @property
    def cdr_reference(self):
        return self._cdr_reference

    @property
    def imei(self):
        return self._imei

    @property
    def session_status(self):
        return self._session_status

    @property
    def momsn(self):
        return self._momsn

    @property
    def mtmsn(self):
        return self._mtmsn

    @property
    def time_of_session(self):
        return self._time_of_session


class MobileOriginatedPayload(InformationElement):

    def __init__(self, id_, length, data):
        super(MobileOriginatedPayload, self).__init__(id_, length, data)
        self._payload  = data

    @property
    def payload(self):
        return self._payload


class MobileOriginatedLocationInformation(InformationElement):
    def __init__(self, id_, length, data):
        raise NotImplemented


class MobileTerminatedHeader(InformationElement):
    def __init__(self, id_, length, data):
        raise NotImplemented


class MobileTerminatedPayload(InformationElement):
    def __init__(self, id_, length, data):
        raise NotImplemented


class MobileTerminatedConfirmationMessage(InformationElement):
    def __init__(self, id_, length, data):
        raise NotImplemented
