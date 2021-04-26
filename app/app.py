#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask
from flask import request, render_template, redirect, url_for, flash, make_response, g
import json
import requests
import hashlib
from markupsafe import escape
import os

app = flask.Flask(__name__)

def to_json(data):
	return json.dumps(data) + "\n"

def response(code, data):
	return flask.Response(
		status=code,
		mimetype="application/json",
		response=to_json(data)
	)

def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code

@app.errorhandler(404)
def page_not_found(e):
    return response(400, {"result": {"status": "error", "code": 400, "message": "File name not specified!"}})

@app.route('/')
def index():
	return flask.redirect('/api/v1/auth/')

@app.route('/api/v1/auth/<username>/<password>/<filename>/<diallist>/', methods=['GET', 'POST'])
def auth(username, password, filename, diallist):
	if escape(username) == "admin" and escape(password) == "admin":
		out_file = "uploads/{0}.txt".format(escape(filename))
		lists = escape(diallist)
		# print(lists)
		with open(out_file, "w") as file:
			for line in  lists:
				print(line)
				file.write(str(line.split(',')))
		return response(200, {"result": {"status": "ok", "code": 200, "message": "Ok!"}})


		# if request.args:
		# 	args = request.args
		# 	serialized = ", ".join("{0}: {1}".format(k,v) for k, v in request.args.items())
		# 	# print(to_json(serialized))
		# 	# print(escape(name_file))
		# 	# return '{}\'s profile'.format(escape(username))
		# 	return "(Query) {0}".format(to_json(serialized)), 200
		# else:
		# 	# return "No query string received", 200
		# 	return response(200, {"result": {"status": "error", "code": 204, "message": "No content!"}})
		# if request.method == 'POST':
		# 	return redirect(url_for('test', username=username, password=password))
		# else:
		# 	return render_template('auth.html')
	else:
		return response(401, {"result": {"status": "error", "code": 401, "message": "Unauthorized!"}})
		# return response(affected_num_to_code(cnt), {})

# @app.route('/test/', methods=['POST'])
# def test():
# 	username = request.form['username']
# 	password = request.form['password']
# 	if username == 'admin' and password == 'admin':
# 		# return render_template('test.html')
# 		res = make_response(render_template('test.html'))
# 		res.set_cookie("user", username, max_age=60*60*24*365*2)
# 		return res
# 	else:
# 		return response(401, {"result": {"status": "error", "code": 401, "message": "Unauthorized!"}})

if __name__ == '__main__':
	app.run(debug=True)


# username = request.args.get('username')
# password = request.args.get('password')
# return username
# это всё говнокодерство. я решил сделать бота в телеграм для того чтобы тот выдавал токен и по токену происходила авторизация