from flask import Flask,request ,render_template
import pdb

app = Flask(__name__)

@app.route("/home/")
def hello_world():
	name_str = request.args.get('name')
	age_str = request.args['age']
	#return "Congrats " +name_str
	return render_template('welcome.html',name = name_str,age=age_str)
@app.route("/buy",methods=['POST'])
def buy_and_sale():
	#pdb.set_trace()
	post_value =request.form["post_parameter1"]
	return "Congrates!" +post_value

if (__name__=="__main__"):
	app.run()
