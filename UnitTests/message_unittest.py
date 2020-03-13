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
        my_random_unicode_str = MessagesUnitTest.random_utf8(length=12)
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
        rp = ReadWriteProcess(action=Action.Read, messages_number=70)
        wp.run()
        read_results = rp.run()
        wp.wait_for_other()
        rp.wait_for_other()
        for message in read_results:
            if message not in messages:
                self.fail('This message {0} was not written'.format(message))

    @staticmethod
    def random_utf8(length):
        return u''.join(unichr(random.randint(0x80, sys.maxunicode)) for _ in range(length))
