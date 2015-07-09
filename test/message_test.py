from sbd import Message


def read_test():
    message = Message.read("data/test.sbd")
    assert message.protocol_revision_number == 1
    assert message.overall_message_length == 56
    assert message.data == "test message from pete"
