import unittest
import random
import string
from infra.read_write_process import ReadWriteProcess, Action

class MessagesUnitTest(unittest.TestCase):



    def test_equal(self):
        s = string.lowercase + string.uppercase + string.digits
        message = ''.join(random.sample(s, 10))
        wp = ReadWriteProcess(action=Action.Write, messages_number=1, message=message)
        rp = ReadWriteProcess(action=Action.Read, messages_number=1)
        wp.run()
        read_result = rp.run()
        wp.wait_for_other()
        rp.wait_for_other()
        self.assertEqual(message, read_result[0], 'Actual: {0} Received: {1} Values are not Equal'.format(message, read_result))

