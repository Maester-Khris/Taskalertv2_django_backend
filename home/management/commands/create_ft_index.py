from django.core.management.base import BaseCommand
from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
from pymongo.errors import OperationFailure
from django.conf import settings

class Command(BaseCommand):
    print("=========== Create a full-text search index on tasks collections =======")
    
    def handle(self, *args, **kwargs):
        client = MongoClient(settings.MONGO_CONNECTION_URI)
        tasksdatabase = client[settings.MONGO_DATABASE_NAME]
        taskcollection = tasksdatabase[settings.MONGO_COLLECTION_NAME]

        search_index_model = SearchIndexModel(
            definition={
                "mappings": {
                    "dynamic": False,
                    "fields":{
                        "title": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string"
                        },
                        "items": {
                            "type": "string"
                        }
                    }
                },
            },
            name="tasks-ft-search",
        )
        try:
            result = taskcollection.create_search_index(model=search_index_model)
            print(result)
        except OperationFailure as e:
            print(f"An error occurred: {e}")