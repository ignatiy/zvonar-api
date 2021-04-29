#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import flask
from flask import request, render_template, redirect, url_for, flash, make_response, g
import json
import requests
import hashlib
from markupsafe import escape
import os
import config
# from app import config

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
    return response(400, {"result": {"status": "error", "code": 400, "message": "Bad Request!"}})

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return response(405, {"result": {"status": "error", "code": 405, "message": "Method Not Allowed!"}})
	else:
		return response(403, {"result": {"status": "error", "code": 403, "message": "Forbidden!"}})

@app.route('/api/v1/call/<username>/<password>/<filename>/<diallist>/', methods=['GET', 'POST'])
def call(username, password, filename, diallist):
	if request.method == 'GET':
		if escape(username) == config.username and escape(password) == config.password:
			out_file = "{0}{1}.txt".format(config.dir_upload, escape(filename))
			lists = [str(escape(diallist))]
			if os.path.exists(out_file):
				for lines in lists:
					with open(out_file, "a") as file:
						file.write(lines.replace(',', '\n'))
					with open(out_file, "a") as file:
						file.write('\n')
			else:
				for lines in lists:
					with open(out_file, "w") as file:
						file.write(lines.replace(',', '\n'))
					with open(out_file, "a") as file:
						file.write('\n')
			return response(200, {"result": {"status": "success", "code": 200, "message": "Ok! Dialing into the ringer zvonar"}})
		else:
			return response(401, {"result": {"status": "error", "code": 401, "message": "Unauthorized!"}})
	else:
		return response(403, {"result": {"status": "error", "code": 403, "message": "Forbidden!"}})

if __name__ == '__main__':
	app.run(debug=True)