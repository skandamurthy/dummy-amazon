from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient()
db = client['webdatabase']
ans = []
def buyer_products():
	result1 = db["products"].find({})	
	for post in result1:
		ans.append(post)
	return ans
	
def cart_details(user_id):
	cart_list =[]
	#print(product_id)
	filter_query1 = {"_id":user_id}
	results = db["users"].find_one(filter_query1)
	return results

def update_cart_details(user_id,product_id):
	print(product_id)
	print(user_id)
	return db["users"].update({"_id":ObjectId(user_id)},{"$addToSet":{"cart_details":[product_id]}})

	
#print(buyer_products()) 	
