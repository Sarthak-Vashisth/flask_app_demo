from flask import Flask, jsonify, request
from google.cloud import ndb
from flask_restful import Api, Resource

app=Flask(__name__)
api = Api(app)


class SampleUser(ndb.Model):
	name = ndb.StringProperty()
	email = ndb.StringProperty()
	phone = ndb.StringProperty()
	sex = ndb.StringProperty()
	address = ndb.StringProperty()


class UserApi(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user_name = json_data['name']
		user_email = json_data['email']
		user_phone = json_data['phone']
		user_sex = json_data['sex']
		user_address = json_data['address']
		client = ndb.Client()
		with client.context():
			user_info = SampleUser(name=user_name, email=user_email,phone=user_phone,sex=user_sex,address=user_address)
			user_info.put()

class GetUserData(Resource):
	def get(self):
		user_list=[]
		query = SampleUser.query()
		print(query)
		client = ndb.Client()
		with client.context():
			for _ in query:
				user_temp_obj = {}
				user_temp_obj['name'] = _.name
				user_temp_obj['email'] = _.email
				user_temp_obj['phone'] = _.phone
				user_temp_obj['sex'] = _.sex
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