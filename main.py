from flask import Flask, jsonify, request
from google.cloud import ndb
from flask_restful import Api, Resource

app=Flask(__name__)
api = Api(app)



#AIzaSyB6Qp7R6BAFoDD93L0wG_EEhY7oQuQXf3I
class User(ndb.Model):
	firstname = ndb.StringProperty()
	lastname = ndb.StringProperty()
	username = ndb.StringProperty()
	password = ndb.StringProperty()
	email = ndb.StringProperty()
	phone = ndb.StringProperty()
	address = ndb.StringProperty()


class UserApi(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		firstname = json_data['firstname']
		lastname = json_data['lastname']
		user_name = json_data['username']
		user_pwd = json_data['password']
		user_email = json_data['email']
		user_phone = json_data['phone']
		user_address = json_data['address']
		client = ndb.Client()
		with client.context():
			user_info = User(firstname=firstname,lastname=lastname,username=user_name, password=user_pwd,email=user_email,phone=user_phone,address=user_address)
			user_info.put()


class GetUserData(Resource):
	def get(self):
		user_list=[]
		json_data = request.get_json(force=True)
		user_name = json_data['username']
		query = User.query().filter(User.username == user_name)
		print(query)
		client = ndb.Client()
		with client.context():
			for _ in query:
				user_temp_obj = {}
				user_temp_obj['firstname'] = _.firstname
				user_temp_obj['lastname'] = _.lastname
				user_temp_obj['username'] = _.username
				user_temp_obj['email'] = _.email
				user_temp_obj['phone'] = _.phone
				user_temp_obj['address'] = _.address
				user_list.append(user_temp_obj)
		return jsonify(user_list)


api.add_resource(UserApi, '/save_user_data')
api.add_resource(GetUserData, '/get_user_data')

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
    app.run()
# [END gae_python38_app]