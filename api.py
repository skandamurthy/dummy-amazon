from flask import Flask, request ,render_template , redirect , url_for,session
from models.user_model import user_signup,search_user_by_username,check_user
from models.seller_model import new_product,seller_products
from models.buyer_model import buyer_products,cart_details,update_cart_details,update_cart_in_cartpage
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
english_bot.set_trainer(ChatterBotCorpusTrainer)
english_bot.train("chatterbot.corpus.english.greetings")

app = Flask(__name__)
app.secret_key = 'skanda'

@app.route("/")
def index():
	if ("user_id" in session.keys()):
		return render_template('welcome.html', login = "True")
	else:
		return render_template('welcome.html' , login = "False")


@app.route("/login",methods = ['POST'])
def login():
	inbound_username = request.form["username"]
	existing_user = search_user_by_username(inbound_username)
	if(existing_user is None):
		return render_template('error.html', message = 'Not a user,Sign-up to login')
	elif(request.form['password'] == existing_user['password']):
		#print(existing_user)
		session['user_id'] = str(existing_user['_id'])
		session['account_type'] = str(existing_user['account_type'])
		session['username'] = existing_user['username']
		return redirect(url_for('index'))
	else:
		return render_template('error.html', message = "user name or password invaild")

@app.route('/logout')
def logout():
	session.pop('user_id' , None)
	return redirect(url_for('index'))

@app.route('/signup', methods = ['POST'])
def signup():
	user_info = {}
	user_info["name"] = request.form["name"]
	user_info["username"] = request.form["username"]
	user_info["password"] = request.form["password"]
	user_info["email"] = request.form["email"]
	user_info["account_type"] = request.form["account_type"]
	user_info["total"] = 0
	if user_info["account_type"] == "buyer":
		user_info["cart"] = {}
	if check_user(user_info["username"]) is None:
		results = user_signup(user_info)
		if (results is True):
			session['user_id'] = str(user_info['_id'])
			return redirect(url_for('index'))
	else:
		return render_template('error.html',message = 'signup failed')


@app.route("/all_products")
def products_function():
	if session["account_type"] == "seller":
		result = seller_products(session["user_id"])
	else:
		result = buyer_products()
	return render_template("products.html" ,result=result)

@app.route('/add_products')
def func():
	return render_template("add_products.html")

@app.route('/product_details', methods = ['POST'])
def add_product_page():
	product_info = {}
	product_info["name"] = request.form["name"]
	product_info["price"] = request.form["price"]
	product_info["description"] = request.form["description"]
	product_info["user_id"] = session["user_id"]
	product_info["username"] = session["username"]	
	new_product(product_info)
	return redirect(url_for("products_function"))			

@app.route('/add_to_cart', methods = ['POST'])
def add_to_cart():
	#import pdb;pdb.set_trace()
	product_id = request.form["product_id"]
	quantity = request.form["quantity"]
	update_cart_details(session["user_id"],product_id,quantity)
	total_cost(price,quantity,session["total"])
	#print(res)
	return redirect(url_for("cart_page"))

@app.route('/remove_item', methods = ['POST'])
def remove_items():
	product_id =request.form["product_id"]
	quantity = request.form["quantity"]
	update_cart_in_cartpage(product_id,session["user_id"],quantity)
	return redirect(url_for("cart_page"))

@app.route('/cart_page')
def cart_page():
	cart_dict= cart_details(session["user_id"])
	return render_template("cart_page.html",cart_dict = cart_dict)
@app.route('/chatterbot')
def chatterbot():
	userText = request.args.get('msg')
	return render_template("welcome.html",message=str(english_bot.get_response(userText)))
	

if (__name__=="__main__"):
	app.run(debug = True)
