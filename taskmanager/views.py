from django.shortcuts import render
from .utils import get_db_handle


# Create your views here.
def index(request):
    mongodb, mongoclient = get_db_handle()

    collection_name = mongodb["medicinedetails"]

    #let's create two documents
    # medicine_1 = {
    #     "medicine_id": "RR000123456",
    #     "common_name" : "Paracetamol",
    #     "scientific_name" : "",
    #     "available" : "Y",
    #     "category": "fever"
    # }
    # medicine_2 = {
    #     "medicine_id": "RR000342522",
    #     "common_name" : "Metformin",
    #     "scientific_name" : "",
    #     "available" : "Y",
    #     "category" : "type 2 diabetes"
    # }
    # collection_name.insert_many([medicine_1,medicine_2])

    count = collection_name.count_documents(filter={})
    print(f"the number of existing dcument is {count}")