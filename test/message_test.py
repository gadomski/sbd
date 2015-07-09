from sbd import Message


def read_test():
    message = Message.read("data/test.sbd")
    assert message.protocol_revision_number == 1
    assert message.overall_message_length == 56

    header = message.get_information_element(0)
    assert header.id_ == 1
    assert header.length == 28
    assert header.cdr_reference == 0
    assert header.imei == "0"
    assert header.session_status == None
    assert header.momsn == None
    assert header.mtmsn == None
    assert header.time_of_session == None

    assert message.data == "test message from pete"
