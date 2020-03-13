from message_manager import MessageManager
import multiprocessing
import enum


class Action(enum.Enum):
    Write = 1
    Read = 2


class ReadWriteProcess(object):

    def __init__(self, action, messages_number, message=None):
        """
        :param Action(action):
        :param int(messages_number):
        """
        self.messages_number = messages_number
        self.action = action
        self.p = None
        self.message = message

    def run(self):
        manager = multiprocessing.Manager()
        return_results = manager.list()
        self.p = multiprocessing.Process(target=self._execute_action, args=(0, return_results))
        self.p.start()
        return return_results

    def wait_for_other(self):
        self.p.join()

    def _execute_action(self, i, return_results):
        for i in range(self.messages_number):
            if self.action == Action.Read:
                read_message = MessageManager.read_msg(i)
                return_results.append(read_message)
            else:
                if self.message:
                    MessageManager.write_msg(self.message)
                else:
                    self.message = 'My Message #: ' + str(i + 1)
                    MessageManager.write_msg('My Message #: ' + str(i + 1))
                return_results.append(self.message)

