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
	#print(product_id)
	results = []
	filter_query1 = {"_id":ObjectId(user_id)}
	result = db["users"].find_one(filter_query1)
	cart_list=result["cart_details"]
	for item in cart_list:
		filter_query2 = {"_id":ObjectId(item)}
		results.append(db["products"].find_one(filter_query2))
	return results

def update_cart_details(user_id,product_id):
#return a message	
	#print(product_id)
	#print(user_id)
	db["users"].update({"_id":ObjectId(user_id)},{"$addToSet":{"cart_details":{"$each":[product_id]}}})

	
#print(buyer_products()) 	
