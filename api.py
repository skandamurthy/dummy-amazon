from flask import Flask, request ,render_template , redirect , url_for,session
from models.user_model import user_signup,search_user_by_username,check_user
from models.seller_model import new_product

app = Flask(__name__)
app.secret_key = 'skanda'
@app.route("/")
def index():
	if ("user_id" in session.keys()):
		return render_template('welcome.html', login="True")
	else:
		return render_template('welcome.html' , login="False")


@app.route("/login",methods=['POST'])
def login():
	inbound_username = request.form["username"]
	existing_user = search_user_by_username(inbound_username)
	if(existing_user is None):
		return render_template('error.html', message='Not a user,Sign-up to login')
	elif(request.form['password']==existing_user['password']):
		#print(existing_user)		
		session['user_id'] =str(existing_user['_id'])
		session['account_type'] = str(existing_user['account_type'])
		return redirect(url_for('index'))
	else:
		return render_template('error.html', message = "user name or password invaild")

@app.route('/logout')
def logout():
	session.pop('user_id' ,None)
	return redirect(url_for('index'))

@app.route('/signup', methods = ['POST'])
def signup():
	user_info = {}
	user_info["username"] = request.form["username"]
	user_info["password"] = request.form["password"]
	user_info["email"] = request.form["email"]
	user_info["account_type"] = request.form["account_type"]
	if check_user(user_info["username"]) is None:
		results = user_signup(user_info)
		if (results is True):
			session['user_id'] = str(user_info['_id'])
		return redirect(url_for('index'))
	

@app.route("/all_products")
def products_function():
	return render_template("products.html")	

@app.route('/add_products')
def func():
	return render_template("add_products.html")	

@app.route('/product_details', methods = ['POST'])
def add_product_page():
	product_info = {}
	product_info["name"] =request.form["name"]
	product_info["price"] = request.form["price"]
	product_info["description"] = request.form["description"]
	new_product(product_info)	
	return render_template("products.html")


if (__name__=="__main__"):
	app.run(debug=True)
