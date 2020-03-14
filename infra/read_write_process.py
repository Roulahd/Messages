from message_manager import MessageManager
import multiprocessing
import enum
from infra.utils import Utils
import os

# Enum for process type (read/write)
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
        if action is Action.Write:
            file_name = Utils.get_params()['TextFile']
            os.remove(file_name)

    def get_process(self):
        """
        This method creates read/write processes
        :return: read/written values
        """
        manager = multiprocessing.Manager()
        return_results = manager.list()
        self.p = multiprocessing.Process(target=self._execute_action, args=(0, return_results))
        return return_results, self.p

    def _execute_action(self, i, return_results):
        """
        This method executes read/write processes
        :param return_results: shared data between current process and main process
        """
        if self.messages:
            if self.messages_number > len(self.messages):
                self.messages_number = len(self.messages)
        for i in range(self.messages_number):
            if self.action == Action.Read:
                return_result = MessageManager.read_msg(i)
                return_results.append(return_result)
            elif self.action == Action.Write:
                if self.messages:
                    return_result = self.messages[i]
                    MessageManager.write_msg(self.messages[i])
                else:
                    return_result = 'My Message #: ' + str(i + 1)
                    MessageManager.write_msg('My Message #: ' + str(i + 1))
                return_results.append(return_result)

    def _validate_input(self):
        """
        This method validates process is not executed with invalid inputs and raises errors accordingly
        """
        if not isinstance(self.action, Action):
            raise ValueError("Unknown Action")
        if not isinstance(self.messages_number, int):
            raise ValueError("Message Number is not an Integer")
        elif self.messages_number <= 0:
            raise ValueError("Message Number is Negative or Zero")
        if not isinstance(self.messages, list) and self.messages is not None:
            raise ValueError("Messages are not list or None")
