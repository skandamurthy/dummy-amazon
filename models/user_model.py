from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient()
db = client['webdatabase']

def user_signup(user_info):
	#Here we have to save the user_info dict inside mongo
	results = db['users'].insert_one(user_info)
	return True

def search_user_by_username(username):
	filter_query = {'username' : username}
	results = db["users"].find(filter_query)
	if(results.count() > 0):
		return results.next()
	
	else:
		return None

def check_user(username):
	filter_query = {'username' :username}
	results= db['users'].find(filter_query)

	if(results.count()>0):
		return results.next()

	else:
		return None
