from flask import Flask

app=Flask(__name__)

@app.route("/")
def hello():
	str1 = """<h1>Welcome to flask Blog</h1>
			<p>This is sample</p>
	"""
	return str1

@app.route("/")
def home():
	str1 = '<h1>Welcome to home</h1>'
	return str1


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run()
# [END gae_python38_app]