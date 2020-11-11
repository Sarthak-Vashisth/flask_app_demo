from flask import Flask, jsonify, request, json
from google.cloud import ndb, datastore
from flask_restful import Api, Resource
#import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
from functools import wraps
import datetime
import requests
import logging

app=Flask(__name__)
api = Api(app)

firebaseConfig = {
    "apiKey": "AIzaSyB6Qp7R6BAFoDD93L0wG_EEhY7oQuQXf3I",
    "authDomain": "flask-app-backend-updated.firebaseapp.com",
    "databaseURL": "https://flask-app-backend-updated.firebaseio.com",
    "projectId": "flask-app-backend-updated",
    "storageBucket": "flask-app-backend-updated.appspot.com",
    "messagingSenderId": "800837754379",
    "appId": "1:800837754379:web:850df6e4b3b11336fc710e",
    #"serviceAccount": "C:/Users/sarth/Downloads/flask-app-backend-updated-firebase-adminsdk-h5zoj-d27f731c99.json"
 };

# firebase = pyrebase.initialize_app()

#cred = credentials.Certificate("C:/Users/sarth/Downloads/flask-app-backend-updated-firebase-adminsdk-h5zoj-d27f731c99.json")
firebase_app = firebase_admin.initialize_app("/home/sarthak_vashisth15/flask_app_demo/flask-app-backend-updated-firebase-adminsdk-h5zoj-d27f731c99.json")
auth = firebase_admin.auth.Client(firebase_app)
# firebase_auth=firebase.auth()

##################### Models ####################################
class Commodities_names(ndb.Model):
	commodity_id = ndb.StringProperty()
	commodity_name = ndb.StringProperty()
	record_status = ndb.StringProperty()

class Commodities_buy_sell(ndb.Model):
	user_id = ndb.StringProperty()
	commodity_name = ndb.StringProperty()
	buy_or_sell = ndb.StringProperty()
	price = ndb.IntegerProperty()
	buy_sell_date = ndb.DateTimeProperty()
	created_by = ndb.StringProperty()
	created_on = ndb.DateTimeProperty()
	created_reference_id = ndb.StringProperty()
	deleted_by = ndb.StringProperty()
	deleted_on = ndb.DateTimeProperty()
	deleted_reference_id = ndb.StringProperty()
	record_status = ndb.StringProperty()

################## Models ######################################

@app.route('/api/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'message': 'Error missing email or password'},400
    try:
        user = auth.create_user(
               email=email,
               password=password
        )
        return {'message': f'Successfully created user'},200
    except Exception as e:
        print(e)
       	return {'message': 'Error creating user'},400

#Api route to get a new token for a valid user
@app.route('/api/token')
def token():
	email = request.form.get('email')
	password = request.form.get('password')
	logger = logging.getLogger(__name__)
	try:
		# user = firebase_auth.sign_in_with_email_and_password(email, password)
		#print(dir(user.items()))
		#firebase_auth.send_email_verification(user['idToken'])
		#print(firebase_auth.get_account_info(user['idToken']))
		# firebase_auth.create_custom_token(user['users'][0])
		print(dir(credentials))
		print(credentials.service_account)
		# print(dir(firebase_app.credential.get_credential()))
		# print(firebase_app.credential.get_access_token())
		logger.info("email ----> %s",email)
		request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(firebaseConfig['apiKey'])
		headers = {"content-type": "application/json; charset=UTF-8"}
		data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
		response_object = requests.post(request_ref, headers=headers, data=data)
		response_json = response_object.json()
		jwt = response_json['idToken']
		print(jwt)
		return {'token': jwt}, 200
	except Exception as e:
		print(e)
		logger.error("There was an error logging in: %s", e)
		return {'message': 'There was an error logging in {}'.format(e)},400

def check_token(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if not request.headers.get('authorization'):
			return {'message': 'No token provided'},400
		try:
			user = auth.verify_id_token(request.headers['authorization'])
			request.user = user
		except Exception as e:
			print(e)
			return {'message':'Invalid token provided. here'},400
		return f(*args, **kwargs)
	return wrap


#AIzaSyB6Qp7R6BAFoDD93L0wG_EEhY7oQuQXf3I
# class User(ndb.Model):
# 	firstname = ndb.StringProperty()
# 	lastname = ndb.StringProperty()
# 	username = ndb.StringProperty()
# 	password = ndb.StringProperty()
# 	email = ndb.StringProperty()
# 	phone = ndb.StringProperty()
# 	address = ndb.StringProperty()


# class UserApi(Resource):
# 	def post(self):
# 		json_data = request.get_json(force=True)
# 		firstname = json_data['firstname']
# 		lastname = json_data['lastname']
# 		user_name = json_data['username']
# 		user_pwd = json_data['password']
# 		user_email = json_data['email']
# 		user_phone = json_data['phone']
# 		user_address = json_data['address']
# 		client = ndb.Client()
# 		with client.context():
# 			user_info = User(firstname=firstname,lastname=lastname,username=user_name, password=user_pwd,email=user_email,phone=user_phone,address=user_address)
# 			user_info.put()


@app.route('/get_commodity_names',methods=['GET'])
@check_token
def get_commodity_names():
	if request.method == 'GET':
		try:
			default_response={}
			if request.user['uid']:
				commodity_name_list = []
				print("asdasdsad")
				client = ndb.Client()
				with client.context():
					commodity_names = Commodities_names.query().filter(Commodities_names.record_status=='Active')#.order(Commodities_names.commodity_id)
					for _ in commodity_names:
						commodity_temp_obj = {}
						commodity_temp_obj['commodity_id'] = _.commodity_id
						commodity_temp_obj['commodity_name'] = _.commodity_name
						commodity_temp_obj['record_status'] = _.record_status
						commodity_name_list.append(commodity_temp_obj)

			else:
				default_response['response_code'] = 400	
				default_response['response_data'] = "User not registered or session expired"
				response = app.response_class(
						response=json.dumps(default_response),
						status=400,
						mimetype='application/json'
						)
				return response
			default_response['response_description'] = commodity_name_list
			default_response['response_code'] = 200
			response = app.response_class(
						response=json.dumps(default_response),
						status=200,
						mimetype='application/json'
						)
			return response
		except Exception as e:
			print(e)
			default_response['response_description'] = "Exception occured while saving data"
			default_response['response_code'] = 500
			response = app.response_class(
						response=json.dumps(default_response),
						status=500,
						mimetype='application/json'
						)
			return response


@app.route('/create_commodity_data',methods=['POST'])
@check_token
def create_commodity_data():
	if request.method == 'POST':
		try:
			format = "%d/%m/%Y %H:%M:%S"
			default_response={}
			print(request.get_json(force=True))
			incoming_req_obj = request.get_json()
			print(request.user['uid'])
			print(incoming_req_obj)
			commodity_name = incoming_req_obj['commodity_name']
			buy_or_sell = incoming_req_obj['buy_or_sell']
			price = incoming_req_obj['price']
			buy_sell_date = datetime.datetime.strptime(incoming_req_obj['buy_sell_date'], format)
			created_by = request.user['email']
			created_on = datetime.datetime.now()
			created_reference_id = "12345"
			record_status = 'Active'
			if request.user['uid']:
				client = ndb.Client()
				with client.context():
					# client = datastore.Client()
					# #key = client.key(kind,"Commodities_buy_sell")
					# task = datastore.Entity()
					# task['user_id'] = request.user['uid']
					# task['commodity_name'] = commodity_name
					# task['buy_or_sell'] = buy_or_sell
					# task['price'] = price
					# task['buy_sell_date'] = buy_sell_date
					# task['created_by'] = created_by
					# task['created_on'] = created_on
					# task['created_reference_id'] = created_reference_id
					# task['deleted_by'] = deleted_by
					# task['deleted_on'] = deleted_on
					# task['deleted_reference_id'] = deleted_reference_id
					# task['record_status'] = record_status
					# client.put(task)
					commodity = Commodities_buy_sell(user_id=request.user['uid'], 
										commodity_name=commodity_name,buy_or_sell=buy_or_sell,
										price=price,buy_sell_date=buy_sell_date,
										created_by=created_by,created_on=created_on,
										created_reference_id=created_reference_id,
										record_status=record_status)
					commodity.put()
			# print('Saved {}: {}'.format(task.key.name, task['user_id']))
			else:
				default_response['response_code'] = 400	
				default_response['response_data'] = "User not registered or session expired"
				response = app.response_class(
						response=json.dumps(default_response),
						status=400,
						mimetype='application/json'
						)
				return response
			default_response['response_description'] = "Commodity details saved successfully"
			default_response['response_code'] = 200
			response = app.response_class(
						response=json.dumps(default_response),
						status=200,
						mimetype='application/json'
						)
			return response
		except Exception as e:
			print(e)
			default_response['response_description'] = "Exception occured while saving data"
			default_response['response_code'] = 500
			response = app.response_class(
						response=json.dumps(default_response),
						status=500,
						mimetype='application/json'
						)
			return response


@app.route('/get_commodity_data',methods=['GET'])
@check_token
def get_commodity_data():
	if request.method == 'GET':
		try:
			default_response={}
			user_id = request.user['uid']
			query = Commodities_buy_sell.query().filter(Commodities_buy_sell.user_id == user_id).filter(Commodities_buy_sell.record_status=='Active')
			#print(query)
			commodity_list = []
			if request.user['uid']:
				client = ndb.Client()
				with client.context():
					for _ in query:
						print(dir(_.key))
						print(_.key.id())
						commodity_temp_obj = {}
						commodity_temp_obj['ID'] = _.key.id()
						commodity_temp_obj['commodity_name'] = _.commodity_name
						commodity_temp_obj['buy_or_sell'] = _.buy_or_sell
						commodity_temp_obj['price'] = _.price
						commodity_temp_obj['buy_sell_date'] = _.buy_sell_date
						commodity_temp_obj['created_by'] = _.created_by
						commodity_temp_obj['record_status'] = _.record_status
						commodity_list.append(commodity_temp_obj)
				default_response['response_data'] = commodity_list
				default_response['response_code'] = 200
			else:
				default_response['response_code'] = 400	
				default_response['response_data'] = "User not registered or session expired"
				response = app.response_class(
						response=json.dumps(default_response),
						status=400,
						mimetype='application/json'
						)
				return response
			response = app.response_class(
						response=json.dumps(default_response),
						status=200,
						mimetype='application/json'
						)
			return response
		except Exception as e:
			print(e)
			default_response['response_description'] = "Exception occured while retrieving commodity data"
			default_response['response_code'] = 500
			response = app.response_class(
						response=json.dumps(default_response),
						status=500,
						mimetype='application/json'
						)
			return response


@app.route('/delete_commodity_data',methods=['POST'])
@check_token
def delete_commodity_data():
	if request.method == 'POST':
		try:
			default_response={}
			incoming_req_obj = request.get_json()
			id = incoming_req_obj['ID']
			print(dir(Commodities_buy_sell))
			if request.user['uid']:
				client = ndb.Client()
				with client.context():
					commodity = Commodities_buy_sell.get_by_id(id)
					commodity.record_status = 'Deleted'
					commodity.put()
					print(commodity)
				default_response['response_description'] = "Commodity details deleted successfully"
				default_response['response_code'] = 200
			else:
				default_response['response_code'] = 400	
				default_response['response_data'] = "User not registered or session expired"
				response = app.response_class(
						response=json.dumps(default_response),
						status=400,
						mimetype='application/json'
						)
				return response
			response = app.response_class(
						response=json.dumps(default_response),
						status=200,
						mimetype='application/json'
						)
			return response
		except Exception as e:
			print(e)
			default_response['response_description'] = "Exception occured while saving data"
			default_response['response_code'] = 500
			response = app.response_class(
						response=json.dumps(default_response),
						status=500,
						mimetype='application/json'
						)
			return response

# @app.route('/get_user_data',methods=['GET'])
# @check_token
# def get_user_date():
# 	if request.method == 'POST':
# 		print("POST Method")
# 	elif request.method == 'GET':
# 		try:
# 			user_list=[]
# 			print("Helooaksdnaj")
# 			if request.user.uid:
# 				pass
# 			# json_data = request.get_json(force=True)
# 			# print("json_data ---->",json_data)
# 			# user_name = json_data['username']
# 			# query = User.query().filter(User.username == user_name)
# 			# print(query)
# 			# client = ndb.Client()
# 			# with client.context():
# 			# 	for _ in query:
# 			# 		user_temp_obj = {}
# 			# 		user_temp_obj['firstname'] = _.firstname
# 			# 		user_temp_obj['lastname'] = _.lastname
# 			# 		user_temp_obj['username'] = _.username
# 			# 		user_temp_obj['email'] = _.email
# 			# 		user_temp_obj['phone'] = _.phone
# 			# 		user_temp_obj['address'] = _.address
# 			# 		user_list.append(user_temp_obj)
# 			# #return jsonify(user_list)
# 			# response = app.response_class(
# 			# 			response=json.dumps(user_list),
# 			# 			status=200,
# 			# 			mimetype='application/json'
# 			# 			)
# 			# return response
# 		except Exception as e:
# 			print(e)
# 			return {'message':'Exception occured'},400


# class GetUserData(Resource):
# 	@check_token
# 	def get(self):
# 		try:
# 			user_list=[]
# 			json_data = request.get_json(force=True)
# 			print("json_data ---->",json_data)
# 			user_name = json_data['username']
# 			query = User.query().filter(User.username == user_name)
# 			print(query)
# 			client = ndb.Client()
# 			with client.context():
# 				for _ in query:
# 					user_temp_obj = {}
# 					user_temp_obj['firstname'] = _.firstname
# 					user_temp_obj['lastname'] = _.lastname
# 					user_temp_obj['username'] = _.username
# 					user_temp_obj['email'] = _.email
# 					user_temp_obj['phone'] = _.phone
# 					user_temp_obj['address'] = _.address
# 					user_list.append(user_temp_obj)
# 			return jsonify(user_list)
# 		except Exception as e:
# 			print(e)


# api.add_resource(UserApi, '/save_user_data')
# api.add_resource(GetUserData, '/get_user_data')

@app.route("/")
def hello():
	str1 = """<h1>Welcome to flask Blog</h1>
			<p>This is sample</p>
	"""
	return str1

@app.route("/home")
def home():
	str1 = '<h1>Welcome to home</h1>'
	return str1


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(debug=True)
# [END gae_python38_app]