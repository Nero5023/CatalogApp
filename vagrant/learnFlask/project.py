from flask import Flask
# from flask.ext.script import Manager
app = Flask(__name__)
# manager = Manager(app)

@app.route('/')
def index():
	return '<h1>Hello Wrold!</h1>'

@app.route('/user/<path:name>')
def user(name):
	return '<h1>Hello,%s!</h1>' % name

if __name__ == '__main__':
	app.debug = True
	manager.run(host='0.0.0.0', port=5000)