#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import datetime
import time
import re
import json
import hashlib

import flask
from flask import request, render_template, redirect, url_for, flash, make_response, g
import requests
from markupsafe import escape

# from app import config
import config

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

@app.route('/api/v1/call/<username>/<password>/<diallist>/<phone_number>/', methods=['GET', 'POST'])
def call(username, password, diallist, phone_number):
	if request.method == 'GET':
		if escape(username) == config.username and escape(password) == config.password:
			out_file = "{0}{1}-{2}.txt".format(config.dir_upload, escape(diallist), str(time.time()))
			lists = str(escape(phone_number)).split(',')
			# lists = ['9000000101','9000000102','8000000102','8000000103','89000000104','900000010a']
			for lines in lists:
				if re.match(r'[9]{1}[0-9]{9}', lines) and len(lines) == 10:
					with open(out_file, "a") as file:
						file.write(lines)
					with open(out_file, "a") as file:
						file.write('\n')
				else:
					return response(200, {"result": {"status": "success", "code": 200, "message": "Some phone numbers were not added to the dialing queue. Make sure the phone number is in 10-digit format without 8" }})
			
			return response(200, {"result": {"status": "success", "code": 200, "message": "The phone number is added to the dialing queue"}})
		else:
			return response(401, {"result": {"status": "error", "code": 401, "message": "Unauthorized!"}})
	else:
		return response(403, {"result": {"status": "error", "code": 403, "message": "Forbidden!"}})

if __name__ == '__main__':
	# app.run(host='0.0.0.0')
	app.run(debug=True)
