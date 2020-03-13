from utils import Utils
import os
import pymongo


class MessageManager(object):

    lock = False
    started = True

    @staticmethod
    def write_msg(msg):
        MessageManager._wait_while_locked()
        # Remove text file only if message manager just started
        MessageManager._clean_data_base()
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
            MessageManager.lock = True
            db = open(file_name, "r")
            lines = db.read().split('\n')
            db.close()
            if len(lines) > index + 1:
                index_msg_found = True
            MessageManager.lock = False

        db = open(file_name, "r")
        result = db.read().split('\n')[index]
        db.close()
        print('[*] READ: ' + result)
        MessageManager.lock = False
        return result

    @staticmethod
    def _clean_data_base():
        """
        Supporting both Text file or MongoDB
        :return:
        """
        run_on = Utils.get_params()['RunOn']
        if run_on == 'TF':
            file_name = Utils.get_params()['TextFile']
            if os.path.exists(file_name) and MessageManager.started:
                os.remove(file_name)
        else:
            my_col = MessageManager._get_collection()
            my_col.delete({})
        MessageManager.started = False

    @staticmethod
    def _wait_while_locked():
        while True:
            if not MessageManager.lock:
                MessageManager.lock = True
                break

    """
    Mongo DB Helper functions
    """
    @staticmethod
    def _get_collection():
        mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")
        my_db = mongodb_client["MyDatabase"]
        my_col = my_db["Messages"]
        return my_col
