from Utils import Utils
import os

class MessageManager(object):

    lock = False

    @staticmethod
    def write_msg(msg):
        while MessageManager.lock:
            print ""
        MessageManager.lock = True
        with open(Utils.get_params()['TextFile'], 'a') as db:
            db.write('{0}\n'.format(msg))
        MessageManager.lock = False

    @staticmethod
    def read_msg(index):
        file_name = Utils.get_params()['TextFile']
        result = 'Empty'

        while MessageManager.lock:
            print "locked in Read"

        while not os.path.exists(Utils.get_params()['TextFile']):
            print ""

        MessageManager.lock = True

        found = False
        while not found:
            db = open(file_name, "r")
            lines = db.read().split('\n')
            db.close()
            if len(lines) > index:
                found = True
        try:
            db = open(file_name, "r")
            result = db.read().split('\n')[index]
            db.close()
        except:
            print 'The Index: ' + str(index)
            for line in db.read().split('\n'):
                print('line: ' + str(line))
        MessageManager.lock = False
        return result
