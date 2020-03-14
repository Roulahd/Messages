from utils import Utils
import os


class MessageManager(object):

    lock = False
    started = True

    @staticmethod
    def write_msg(msg):
        """
        This method writes given or default message on TF
        Will wait for: lock to be false - Because we don't want two processes using the TF in the same time
        :param msg: message to write
        :return:
        """
        MessageManager._wait_while_locked()
        # Remove text file only if message manager just started
        MessageManager._remove_text_file()
        file_name = Utils.get_params()['TextFile']

        with open(file_name, 'a') as db:
            db.write('{0}\n'.format(msg))
            # print('[**] WRITE: ' + msg) # Was only for debugging
        MessageManager.lock = False

    @staticmethod
    def read_msg(index):
        """
        This method reads message given a specific index in regards of TF 
        Will wait for:
        1- lock to be false - Because we don't want two processes using the in the same time
        2- Wait for the entry in the specific index to be written in order to read it,
           Because we may have some cases the read process is ahead of the write process
        :param index: where to read
        :return: return read message
        """
        file_name = Utils.get_params()['TextFile']
        # While File doesn't exist, it will run only once, when Write create the file first time
        while True:
            MessageManager._wait_while_locked()
            if os.path.exists(file_name):
                break
            else:
                MessageManager.lock = False

        index_msg_found = False
        while not index_msg_found:
            db = open(file_name, "r")
            lines = db.read().split('\n')
            db.close()
            if len(lines) > index + 1:
                index_msg_found = True

        db = open(file_name, "r")
        result = db.read().split('\n')[index]
        db.close()
        print('[*] READ: ' + result)
        MessageManager.lock = False
        return result

    @staticmethod
    def _remove_text_file():
        """
        This method deletes TF only on the beginning of program's life
        :return:
        """
        file_name = Utils.get_params()['TextFile']
        if os.path.exists(file_name) and MessageManager.started:
            os.remove(file_name)
            MessageManager.started = False

    @staticmethod
    def _wait_while_locked():
        """
        Current process waits for the lock to be released, once released it will be locked again by the current process
        :return:
        """
        while True:
            if not MessageManager.lock:
                MessageManager.lock = True
                break
