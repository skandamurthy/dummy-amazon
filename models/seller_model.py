from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient()
db = client['webdatabase']

def new_product(product_info):
	res =db["products"].insert_one(product_info)
	return True
