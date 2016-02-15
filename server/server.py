#!/usr/bin/env python

from bottle import route, run, request, error, static_file, response, template
from bottle import HTTPResponse
import urllib2
import json
import md5
import hashlib
import pyscreenshot as ImageGrab
import io
from io import BytesIO
import base64
from easyprocess import EasyProcess
import tempfile
from PIL import Image
import os

from bottle import static_file

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')
    

@route('/getplaylist')
def getplaylist():
	response = urllib2.urlopen('http://localhost:8000/playlist/2')
	data = json.load(response) 
	
	
	
	
	return hashlib.md5(json.dumps(data['data'])).hexdigest()
    
    

    
@route('/splash')
def splash():
    return template('splash')

quality = '30'
	
myenv=dict(os.environ, DISPLAY = ":0")

@route('/screenshot')
def screenshot():

	f = tempfile.NamedTemporaryFile(suffix='.jpg', prefix='_scrot_')
	filename = f.name
	print EasyProcess(['scrot', '-q', quality, filename], env=myenv).call().stderr
	
	with open(filename, "rb") as imageFile:
		image_buffer = imageFile.read()
	response.set_header('Content-type', 'image/jpeg')
	return image_buffer
	
	
@route('/screenshot/thumb')
def screenshot_thumb():

	f = tempfile.NamedTemporaryFile(suffix='.jpg', prefix='_scrot_')
	ft = tempfile.NamedTemporaryFile(suffix='.jpg', prefix='_scrot_thumb_')
	filename = f.name
	tumbname = ft.name
	print EasyProcess(['scrot', '-q', quality, filename], env=myenv).call().stderr
	
	im = Image.open(filename)
	size = 200, 300
	im.thumbnail(size)
	im.save(tumbname, "JPEG")
	
	with open(tumbname, "rb") as imageFile:
		image_buffer = imageFile.read()
	response.set_header('Content-type', 'image/jpeg')
	return image_buffer
	

run(host="0.0.0.0", port=81, fast=True, reloader=True)