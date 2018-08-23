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

#print(buyer_products()) 	
