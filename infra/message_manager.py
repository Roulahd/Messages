from utils import Utils
import os


class MessageManager(object):

    lock = False
    started = True

    @staticmethod
    def write_msg(msg):
        MessageManager._wait_while_locked()
        # Remove text file only if message manager just started
        MessageManager._remove_text_file()
        file_name = Utils.get_params()['TextFile']

        with open(file_name, 'a') as db:
            db.write('{0}\n'.format(msg))
            print('[**] WRITE: ' + msg)
        MessageManager.lock = False

    @staticmethod
    def read_msg(index):
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
        file_name = Utils.get_params()['TextFile']
        if os.path.exists(file_name) and MessageManager.started:
            os.remove(file_name)
            MessageManager.started = False

    @staticmethod
    def _wait_while_locked():
        while True:
            if not MessageManager.lock:
                MessageManager.lock = True
                break
