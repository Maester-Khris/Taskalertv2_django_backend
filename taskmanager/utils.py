import pymongo
from pymongo import MongoClient

def get_db_handle():
    client = MongoClient('mongodb+srv://nk_dev:JlreVIdITFqTbNmK@cluster0.sgdzstx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db = client['taskalertdb']
    return db


def createTask(name, group, description):
    mongodb = get_db_handle()
    task_collection = mongodb["tasks"]
    task = {
        "name": name,
        "group" : group,
        "description" : description,
    }
    task_collection.insert_one(task)

    return 'done'


def listTask():
    mongodb = get_db_handle()
    task_collection = mongodb["tasks"]

    return list(task_collection.find({}))


# task = {
#     "name": "project creation",
#     "group" : "dev projects",
#     "description" : "start building the full stack app",
# }
# task_collection.insert_one(task)
