from utils import Utils
import os
import pymongo


class MessageManager(object):

    lock = False
    started = True
    mongoDBcounter = 1
    mongodb_client = None
    my_col = None

    @staticmethod
    def write_msg(msg):
        run_on = Utils.get_params()['RunOn']
        MessageManager._wait_while_locked()
        MessageManager._clean_data_base()

        if run_on == 'TF':
            # Remove text file only if message manager just started
            file_name = Utils.get_params()['TextFile']
            with open(file_name, 'a') as db:
                db.write('{0}\n'.format(msg))
                print('[**] WRITE: ' + msg)
        else:
            # Remove text file only if message manager just started
            write_msg = {"id": str(MessageManager.mongoDBcounter), "message": msg}
            MessageManager.mongoDBcounter += 1
            col = MessageManager._get_collection()
            col.insert_one(write_msg)
            print('[**] WRITE: ' + msg)

        MessageManager.lock = False

    @staticmethod
    def read_msg(index):
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
            if MessageManager.started:
                MessageManager._clean_mongo_db_databases()
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
        if MessageManager.mongodb_client is None:
            MessageManager.mongodb_client = pymongo.MongoClient("mongodb://localhost:27017/")
            if "MyDatabase" in MessageManager.mongodb_client.list_database_names():
                my_db = MessageManager.mongodb_client.get_database("MyDatabase")
            else:
                my_db = MessageManager.mongodb_client["MyDatabase"]
            if "Messages" in my_db.collection_names():
                MessageManager.my_col = my_db.get_collection("Messages")
            else:
                MessageManager.my_col = my_db["Messages"]
        return MessageManager.my_col

    @staticmethod
    def _clean_mongo_db_databases():
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        client.drop_database('MyDatabase')
        client.drop_database('mydatabase')
