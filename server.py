#!/usr/bin/env python

from bottle import route, run, request, error, static_file, response, template
from bottle import HTTPResponse
import urllib2
import json
import md5
import hashlib

@route('/getplaylist')
def getplaylist():
	response = urllib2.urlopen('http://localhost:8000/playlist/2')
	data = json.load(response) 
	
	
	return hashlib.md5(json.dumps(data['data'])).hexdigest()
    
    
    
    
@route('/splash')
def splash():
    return template('splash')



run(host="0.0.0.0", port=81, fast=True, reloader=True)