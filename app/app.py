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
    return response(400, {"result": {"status": "error", "code": 400, "message": "Parameters not specified!"}})

@app.route('/')
def index():
	return flask.redirect('/api/v1/call/')

@app.route('/api/v1/call/<username>/<password>/<filename>/<diallist>/', methods=['GET', 'POST'])
def call(username, password, filename, diallist):
	if request.method == 'GET':
		if escape(username) == "admin" and escape(password) == "admin":
			out_file = "/media/sysadmin2/Data/Project/zvonar-api/app/uploads/{0}.txt".format(escape(filename))
			lists = [str(escape(diallist))]
			for lines in lists:
				with open(out_file, "w") as file:
					file.write(lines.replace(',', '\n'))
				with open(out_file, "a") as file:
					file.write('\n')
			return response(200, {"result": {"status": "ok", "code": 200, "message": "Ok! Dialing into the ringer zvonar"}})
		else:
			return response(401, {"result": {"status": "error", "code": 401, "message": "Unauthorized!"}})
	else:
		return response(403, {"result": {"status": "error", "code": 403, "message": "Access is denied!"}})

if __name__ == '__main__':
	app.run(debug=True)