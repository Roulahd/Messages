from message_manager import MessageManager
import multiprocessing
import enum


class Action(enum.Enum):
    Write = 1
    Read = 2


class ReadWriteProcess(object):

    def __init__(self, action, messages_number):
        """
        :param Action(action):
        :param int(messages_number):
        """
        self.messages_number = messages_number
        self.action = action
        self.p = None

    def run(self):
        self.p = multiprocessing.Process(target=self._execute_action)
        self.p.start()

    def wait_for_other(self):
        self.p.join()

    def _execute_action(self):
        for i in range(self.messages_number):
            if self.action == Action.Read:
                MessageManager.read_msg(i)
            else:
                MessageManager.write_msg('My Message #: ' + str(i + 1))
