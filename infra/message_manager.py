from utils import Utils
import os
import pymongo


class MessageManager(object):

    lock = False
    mongo_db_counter = 1

    @staticmethod
    def write_msg(msg):
        """
        This method writes given or default message on TF or MongoDB
        Will wait for: lock to be false - Because we don't want two processes using the TF or MongoDB in the same time
        :param msg: message to write
        :return:
        """
        run_on = Utils.get_params()['RunOn']
        MessageManager._wait_while_locked()

        if run_on == 'TF':
            file_name = Utils.get_params()['TextFile']
            with open(file_name, 'a') as db:
                db.write('{0}\n'.format(msg))
                # For debugging only
                # print('[**] WRITE: ' + msg)
        else:
            write_msg = {"id": str(MessageManager.mongo_db_counter), "message": msg}
            MessageManager.mongo_db_counter += 1
            col = MessageManager._get_collection()
            col.insert_one(write_msg)
            # For debugging only
            # print('[**] WRITE: ' + msg)

        MessageManager.lock = False

    @staticmethod
    def read_msg(index):
        """
        This method reads message given a specific index in regards of TF or MongoDB
        Will wait for:
        1- lock to be false - Because we don't want two processes using the TF or MongoDB in the same time
        2- Wait for the entry in the specific index to be written in order to read it,
           Because we may have some cases the read process is ahead of the write process
        :param index: where to read
        :return: return read message
        """
        run_on = Utils.get_params()['RunOn']
        result = ""
        if run_on == 'TF':
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
        else:
            found = False
            query = {"id": str(index + 1)}
            while not found:
                MessageManager._wait_while_locked()
                results = MessageManager._get_collection().find(query)
                if results.count() == 1:
                    result = results[0]['message']
                    print('[*] READ: ' + result)
                    found = True
                MessageManager.lock = False
        return result

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

    """
    Mongo DB Helper functions
    """
    @staticmethod
    def _get_collection():
        """
        This method returns Mongo DB collection
        :return: MongoDB collection
        """
        mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")
        return mongodb_client["MyDatabase"]["Messages"]
