from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client['webdatabase']

def new_product(product_info):
	res =db["products"].insert_one(product_info)
	return True

def seller_products(user_id):
	ans =[]
	filter_query = {'user_id': user_id}
	results = db["products"].find(filter_query)
	for post in results:
		ans.append(post)
	return ans

"""def seller_name(user_id):
	filter_query = {"user_id" :user_id}
	res = db["users"].find_one(filter_query)
	return (res["username"])"""


#seller_products("5b767b32cfcda6160dfb30e9")
