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
            print('Writing: ' + msg)
        MessageManager.lock = False

    @staticmethod
    def read_msg(index):
        MessageManager._wait_while_locked()
        # Remove text file only if message manager just started
        MessageManager._remove_text_file()
        file_name = Utils.get_params()['TextFile']
        while not os.path.exists(file_name):
            print ""
        found = False
        while not found:
            db = open(file_name, "r")
            lines = db.read().split('\n')
            db.close()
            if len(lines) > index:
                found = True

        db = open(file_name, "r")
        result = db.read().split('\n')[index]
        db.close()
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
                break
        MessageManager.lock = True
