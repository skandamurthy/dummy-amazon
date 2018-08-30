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
	quantity_intermediate= {}
	filter_query1 = {"_id" : ObjectId(user_id)}
	result = db["users"].find_one(filter_query1)
	cart_list = result["cart"]
	#zip both quantity and product_id,create a different dictionary and merge them using mapping
	for item,quantity in zip(cart_list.keys(),cart_list.values()): 
		filter_query2 = {"_id" : ObjectId(item)}
		result =db["products"].find_one(filter_query2)
		quantity_intermediate["quantity"] =quantity
		results.append({**result,**quantity_intermediate})
	return results

def update_cart_details(user_id,product_id,quantity):
#return a message	
	#print(product_id)
	#print(user_id)
	#print(quantity)	
	#db["users"].update({"_id":ObjectId(user_id)},{"$addToSet":{"cart_details":{"$each":[{"product_id":product_id,"quantity":quantity}]}}})
	quantity = int(quantity)
	user_info = db["users"].find_one({"_id":ObjectId(user_id)})
	cart_dict = user_info["cart"]
	db["users"].update({"_id" : ObjectId(user_id)},{"$inc" : {"cart."+product_id : quantity}})
#print(buyer_products())

def remove_item(product_id,user_id):
	user_info = db['users'].find_one({"_id":ObjectId(user_id)})
	cart_dict = user_info['cart']
	cart_dict.pop(product_id)
	db["users"].update({"_id": ObjectId(user_id)},{"$unset": {"cart."+product_id: ""}})

