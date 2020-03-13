import unittest
import random, string, sys
from infra.read_write_process import ReadWriteProcess, Action


class MessagesUnitTest(unittest.TestCase):

    def test_equal(self):
        """
        This unit test writes a random string consisted of 10 chars (digits, upper&lower case)
        then reads and validates the value is equal with read process
        """
        s = string.lowercase + string.uppercase + string.digits
        message = ''.join(random.sample(s, 10))
        wp = ReadWriteProcess(action=Action.Write, messages_number=1, messages=[message])
        rp = ReadWriteProcess(action=Action.Read, messages_number=1)
        wp.run()
        read_result = rp.run()
        wp.wait_for_other()
        rp.wait_for_other()
        self.assertEqual(message, read_result[0], 'Actual: {0} Received: {1} Values are not Equal'
                         .format(message, read_result))

    def test_notequal(self):
        """
        This unit test writes a random string consisted of 10 chars (digits, upper&lower case)
        then reads a different string consisted of 9 chars and validates the values are different
        """
        s = string.lowercase + string.uppercase + string.digits
        message = ''.join(random.sample(s, 10))
        wp = ReadWriteProcess(action=Action.Write, messages_number=1, messages=[message])
        written_value = wp.run()
        wp.wait_for_other()
        wrong_value = ''.join(random.sample(s, 9))
        self.assertNotEqual(wrong_value, written_value[0], 'Actual: {0} Received: {1} Values are Equal'
                            .format(wrong_value, written_value[0]))

    def test_utf8(self):
        """
        This unit test writes a random utf8 string consisted of 12 chars
        then reads and validates the value is equal with read process
        """
        my_random_unicode_str = MessagesUnitTest._random_utf8(length=12)
        my_random_utf_8_str = my_random_unicode_str.encode('utf-8')
        wp = ReadWriteProcess(action=Action.Write, messages_number=1, messages=[my_random_utf_8_str])
        rp = ReadWriteProcess(action=Action.Read, messages_number=1)
        wp.run()
        read_result = rp.run()
        wp.wait_for_other()
        rp.wait_for_other()

        try:
            read_result_msg = read_result[0].encode('utf-8')
        except UnicodeDecodeError:
            read_result_msg = read_result[0]

        self.assertEqual(my_random_utf_8_str, read_result_msg,
                         'Actual: {0} Received: {1} Values are not Equal'.format(my_random_utf_8_str, read_result))

    def test_validate_multiple_messages(self):
        """
        This unit test has one write and read processes, then validates read values are actually written
        """
        messages = []
        s = string.lowercase + string.uppercase + string.digits
        for _ in range(100):
            messages.append(''.join(random.sample(s, 10)))
        wp = ReadWriteProcess(action=Action.Write, messages_number=100, messages=messages)
        rp = ReadWriteProcess(action=Action.Read, messages_number=100)
        wp.run()
        read_results = rp.run()
        wp.wait_for_other()
        rp.wait_for_other()
        for message in read_results:
            if message not in messages:
                self.fail('This message {0} was not written'.format(message))

    def test_read_less_than_write(self):
        """
        This unit test reads less than writes and validates that we read all the intended number of messages
        Also validates that every read message is actually from the writen ones
        """
        messages_number_to_write = 200
        messages_number_to_read = 100
        messages = MessagesUnitTest._get_random_messages(messages_number_to_write, 10)
        wp = ReadWriteProcess(action=Action.Write, messages_number=messages_number_to_write, messages=messages)
        rp = ReadWriteProcess(action=Action.Read, messages_number=messages_number_to_read)
        wp.run()
        read_result = rp.run()
        wp.wait_for_other()
        rp.wait_for_other()
        self.assertEqual(messages_number_to_read, len(read_result), 'Actual messages read {0}, Expected {1}'
                         .format(len(read_result), messages_number_to_read))
        for message in read_result:
            if message not in messages:
                self.fail('Message {0} was not actually written'.format(message))

    def test_messages_number_less_than_messages_list(self):
        """
        This unit test writes messages numbers less than messages list sends to the process
        Validate that it writes only messages number from messages list
        """
        messages_number_to_write = 100
        messages_number_to_read = 100
        messages = MessagesUnitTest._get_random_messages(messages_number_to_write + 100, 10)
        wp = ReadWriteProcess(action=Action.Write, messages_number=messages_number_to_write, messages=messages)
        rp = ReadWriteProcess(action=Action.Read, messages_number=messages_number_to_read)
        wp.run()
        read_result = rp.run()
        wp.wait_for_other()
        rp.wait_for_other()
        for message in read_result:
            if message not in messages:
                self.fail('Message {0} was not actually written'.format(message))

    def test_messages_number_greater_than_messages_list(self):
        """
        This unit test writes messages numbers greater than messages list sends to the process
        Validate that it writes only messages list
        """
        messages_number_to_write = 100
        messages_number_to_read = 50
        messages = MessagesUnitTest._get_random_messages(messages_number_to_write - 50, 10)
        wp = ReadWriteProcess(action=Action.Write, messages_number=messages_number_to_write, messages=messages)
        rp = ReadWriteProcess(action=Action.Read, messages_number=messages_number_to_read)
        wp.run()
        read_result = rp.run()
        wp.wait_for_other()
        rp.wait_for_other()
        for message in read_result:
            if message not in messages:
                self.fail('Message {0} was not actually written'.format(message))

    def test_invalid_action(self):
        """
        TODO
        """
        raised = False
        try:
            ReadWriteProcess(action="invalid action", messages_number=1)
        except ValueError:
            raised = True
        self.assertTrue(raised, 'Invalid Action')

    def test_invalid_message_number(self):
        """
        TODO
        """
        raised = False
        try:
            ReadWriteProcess(action=Action.Write, messages_number=-9)
        except ValueError:
            raised = True
        self.assertTrue(raised, 'Invalid messages number')

    def test_invalid_messages(self):
        """
        TODO
        """
        raised = False
        try:
            ReadWriteProcess(action=Action.Write, messages_number=2, messages={1, 2, 3})
        except ValueError:
            raised = True
        self.assertTrue(raised, 'Invalid Messages type')
    """
    Helper Methods
    """
    @staticmethod
    def _random_utf8(length):
        return u''.join(unichr(random.randint(0x80, sys.maxunicode)) for _ in range(length))

    @staticmethod
    def _get_random_messages(messages_number, length):
        messages = []
        s = string.lowercase + string.uppercase + string.digits
        for _ in range(messages_number):
            messages.append(''.join(random.sample(s, length)))
        return messages
