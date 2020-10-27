from flask import Flask

app=Flask(__name__)

@app.route("/")
def hello():
	return 'Hello World!'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run()
# [END gae_python38_app]