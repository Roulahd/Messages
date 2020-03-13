from message_manager import MessageManager
import multiprocessing
import enum


class Action(enum.Enum):
    Write = 1
    Read = 2


class ReadWriteProcess(object):

    def __init__(self, action, messages_number, messages=None):
        """
        :param Action(action):
        :param int(messages_number):
        """
        self.messages_number = messages_number
        self.action = action
        self.p = None
        self.messages = messages
        self._validate_input()

    def run(self):
        manager = multiprocessing.Manager()
        return_results = manager.list()
        self.p = multiprocessing.Process(target=self._execute_action, args=(0, return_results))
        self.p.start()
        return return_results

    def wait_for_other(self):
        self.p.join()

    def _execute_action(self, i, return_results):
        if self.messages:
            if self.messages_number > len(self.messages):
                self.messages_number = len(self.messages)
        for i in range(self.messages_number):
            if self.action == Action.Read:
                read_message = MessageManager.read_msg(i)
                return_results.append(read_message)
            elif self.action == Action.Write:
                if self.messages:
                    MessageManager.write_msg(self.messages[i])
                else:
                    self.messages = 'My Message #: ' + str(i + 1)
                    MessageManager.write_msg('My Message #: ' + str(i + 1))
                return_results.append(self.messages)

    def _validate_input(self):
        if not isinstance(self.action, Action):
            raise ValueError("Unknown Action")
        if not isinstance(self.messages_number, int):
            raise ValueError("Message Number is not an Integer")
        elif self.messages_number <= 0:
            raise ValueError("Message Number is Negative or Zero")
        if not isinstance(self.messages, list) and self.messages is not None:
            raise ValueError("Messages are not list or None")
