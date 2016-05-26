#!/usr/bin/env python

import sqlite3 as lite
import sys
import urllib2
import urllib
import json
import pprint
import requests
import urllib
#from utils import url_fails
from urlparse import urlparse
from requests import get as req_get
from os import path, getenv, utime, makedirs, system
import logging
import datetime
#from subprocess import call

print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

SERVER = 'ts.zamia.co.uk'
CHANNEL = '2'
HOME = '/home/pi'
APP = 'ts'
MEDIA = 'media'


con = None

sha_file = path.join('/tmp', 'latest_playlist_sha')
last_update = None

def validate_url(string):
    """Simple URL verification.

    >>> validate_url("hello")
    False
    >>> validate_url("ftp://example.com")
    False
    >>> validate_url("http://")
    False
    >>> validate_url("http://example.com/logo.png")
    True
    >>> validate_url("https://example.com/logo.png")
    True

    """

    checker = urlparse(string)
    return bool(checker.scheme in ('http', 'https') and checker.netloc)




def url_fails(url):
    """
    Accept 200 and 405 as 'OK' statuses for URLs.
    Some hosting providers (like Google App Engine) throws a 405 at `requests`.
    """
    try:
        if validate_url(url):
            #obj = requests.head(url, allow_redirects=True, timeout=10, verify=settings['verify_ssl'])
            obj = requests.head(url, allow_redirects=True, timeout=10, verify=0)
            assert obj.status_code in (200, 405)
    except (requests.ConnectionError, requests.exceptions.Timeout, AssertionError):
        return True
    else:
        return False


try:
    con = lite.connect(path.join(HOME, APP, 'player.db'))
    
    cur = con.cursor()  
    
    #build database if not exists
    cur.execute('CREATE TABLE if not exists playlist(uri TEXT, type TEXT, url TEXT, start TEXT, stop TEXT, duration INT)')
    cur.execute('CREATE TABLE if not exists meta(id INT, name TEXT, hash TEXT)')
    
    
    #test server connection first (and valid data before dropping playlist)
    
    
    if not url_fails('http://' + SERVER):
        #can connect to server 
        print "Connected"
        
        
    else:
        print "Unable to connect to server " + SERVER
        system("echo Failed to update playlist    | DISPLAY=:0 osd_cat  --pos=bottom --align=right --color=white -f '-*-*-bold-*-*-*-22-*' --offset=-100 --outline=2 --delay=30")
        exit()

    
    
    if last_update is None or last_update < (datetime.now() - timedelta(seconds=1)):

        if not url_fails('http://' + SERVER):
            latest_sha = req_get('http://' + SERVER + '/playlist/' + CHANNEL + '/hash')

            if latest_sha.status_code == 200:
            
            
                print "hash valid"
                #with open(sha_file, 'w') as f:
                #    f.write(latest_sha.content.strip())
                #return True
            else:
                logging.debug('Received non 200-status')
                #return
        else:
            logging.debug('Unable to retreive latest SHA')


    with open(sha_file, 'r') as f:
        current_sha = f.read()
    
    r = requests.get('http://' + SERVER + '/playlist/' + CHANNEL)
    print "hash from web", r.json()['hash']
    print "previous hash", current_sha
    
    if (current_sha != r.json()['hash']):
        print 'Hash changed, update database'
        mymeta = (
            int(r.json()['data']['meta']['id']),
            r.json()['data']['meta']['name'],
            r.json()['hash']
            )
        cur.execute('DELETE FROM playlist')
        cur.execute('DELETE FROM meta')
        cur.execute('VACUUM')
        cur.executemany('INSERT INTO playlist VALUES (:uri, :type, :url, :start, :stop, :duration)', r.json()['data']['playlist'])
        cur.execute('INSERT INTO meta VALUES (:id, :name, :hash)', mymeta)
        con.commit()
        with open(sha_file, 'w') as f:
            f.write(r.json()['hash'])
        print 'Database updated'
    else:
        print 'Hash matched, not updating.'
    
    
    for item in r.json()['data']['playlist']:
        url = item['url']
        mediadir = path.join(HOME,APP,MEDIA)
        if not path.exists(mediadir):
            makedirs(mediadir)
        
        localpath = path.join(mediadir, item['uri'])
        
        #print url
        site = urllib.urlopen(url)
        meta = site.info()
        #print "content-length" , meta.getheaders("Content-Length")[0]
        
        #check if file already exists
        if (path.isfile(localpath)):
            f = open(localpath, "rb")
            #print "File on disk:",len(f.read())
            locallen = len(f.read()) 
            remotelen =  meta.getheaders("Content-Length")[0]
            if (int(locallen) == int(remotelen)):
                #download        
                print "Not downloading %s again" % item['uri']
            else:
                print "Size difference, downloading %s" % url
                urllib.urlretrieve (url, localpath)
            f.close()
        else:
            #download
            print "Downloading %s" % url
            urllib.urlretrieve (url, localpath)
            
             
    #cur.execute('SELECT * from playlist')
    
    #data = cur.fetchone()
    
    #print " %s" % data                
    
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()

