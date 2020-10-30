from flask import Flask

app=Flask(__name__)

@app.route("/<int:id>")
def hello(id):
	str1 = """<h1>Welcome to flask Blog.. id is {0}</h1>
			<p>This is sample</p>
	""".format(id)
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