import pymongo
from infra.read_write_process import ReadWriteProcess,Action
import random, string


def main():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["messages"]
    mycol.delete_many({})
    # for i in range(3):
    #     my_post = {"id": str(i+1), "Message": "Connect Successfully"}

    #     mycol.insert_one(my_post)

    messages = mycol.find()

    for message in messages:
        print(message)
        print(type(message))

if __name__ == "__main__":
    main()
