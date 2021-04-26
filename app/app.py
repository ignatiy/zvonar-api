#!/usr/bin/env python3
import flask
from flask import request, render_template, redirect, url_for, flash, make_response
import json
import requests
import hashlib

app = flask.Flask(__name__)

def to_json(data):
	return json.dumps(data) + "\n"

def response(code, data):
	return flask.Response(
		status=code,
		mimetype="application/json",
		response=to_json(data)
	)

@app.route('/')
def index():
	return flask.redirect('/api/v1/auth/')

@app.route('/api/v1/auth/', methods=['GET', 'POST'])
def auth():
	if request.args:
		args = request.args
		serialized = ", ".join("{0}: {1}".format(k,v) for k, v in request.args.items())
		return "(Query) {0}".format(serialized), 200
	else:
		return "No query string received", 200
	# if request.method == 'POST':
	# 	return redirect(url_for('test', username=username, password=password))
	# else:
	# 	return render_template('auth.html')

@app.route('/test/', methods=['POST'])
def test():
	username = request.form['username']
	password = request.form['password']
	if username == 'admin' and password == 'admin':
		# return render_template('test.html')
		res = make_response(render_template('test.html'))
		res.set_cookie("user", username, max_age=60*60*24*365*2)
		return res
	else:
		return response(400, {"result": {"status": "error", "code": 400, "message": "Authentification failed!"}})

if __name__ == '__main__':
	app.run(debug=True)


# username = request.args.get('username')
# password = request.args.get('password')
# return username