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
import ConfigParser
import socket
from bottle import static_file, redirect


configfile = '/home/pi/ts/player.ini'

Config = ConfigParser.ConfigParser()
if os.path.isfile(configfile):
	Config.read(configfile)
else:
	cfgfile = open(configfile,'w+')
	Config.add_section('player')
	Config.set('player','server','ts.zamia.co.uk')
	Config.set('player','channel','2')
	Config.write(cfgfile)
	cfgfile.close()


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')
    

@route('/getplaylist')
def getplaylist():
	response = urllib2.urlopen('http://localhost:8000/playlist/2')
	data = json.load(response) 
	
	
	
	
	return hashlib.md5(json.dumps(data['data'])).hexdigest()
    
    
@route('/')
def index():
	return template('home', server=Config.get('player','server'), channel=Config.get('player','channel'))

@route('/', method='POST')
def do_save():
	Config.set('player', 'server', request.forms.get('server'))
	Config.set('player', 'channel', request.forms.get('channel'))
	cfgfile = open(configfile,'w+')
	Config.write(cfgfile)
	cfgfile.close()
	redirect('/')

@route('/splash')
def splash():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	host=s.getsockname()[0]
	s.close()
	return template('splash', host=host, server=Config.get('player','server'), channel=Config.get('player','channel'))

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

@route('/reboot')
def reboot():
	os.system('sudo reboot')
	redirect('/')

@route('/shutdown-actual', method='POST')
def shutdown():
	os.system('sudo shutdown -h now')
	return('Shutting down the system!')

@route('/shutdown')
@route('/shutdown-actual', method='GET')
def confirm_shutdow():
	return('Are you sure? <form method="POST" action="/shutdown-actual"><input type=submit value="YES"/></form><a href=/>NO</a>')


run(host="0.0.0.0", port=8080, fast=True, reloader=True)