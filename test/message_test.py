from sbd import MobileOriginatedMessage


def read_test():
    message = MobileOriginatedMessage.read("data/test.sbd")
    assert message.protocol_revision_number == 1
    assert message.overall_message_length == 56

    header = message.get_information_element(0)
    assert header.id_ == 1
    assert header.length == 28
    assert header.cdr_reference == 1894516585, header.cdr_reference
    assert header.imei == "300234063904190", header.imei
    assert header.session_status == 0, header.session_status
    assert header.momsn == 75, header.momsn
    assert header.mtmsn == 0, header.mtmsn
    assert header.time_of_session == 1436465708, header.time_of_session

    assert message.payload == "test message from pete"
