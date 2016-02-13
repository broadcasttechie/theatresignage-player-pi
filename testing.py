#!/usr/bin/env python

import sqlite3 as lite
import sys
import urllib2
import urllib
import json
import pprint
import requests
import urllib
con = None

try:
    con = lite.connect('player.db')
    
    cur = con.cursor()         
    cur.execute('CREATE TABLE if not exists playlist(uri TEXT PRIMARY KEY, type TEXT, url TEXT, start TEXT, stop TEXT)')
    cur.execute('CREATE TABLE if not exists meta(id INT, name TEXT, hash TEXT)')
    
    cur.execute('DELETE FROM playlist')
    cur.execute('VACUUM')
    
    r = requests.get('http://localhost:8000/playlist/2')
    
    print(r.json()['hash'])
    
    cur.executemany('INSERT INTO playlist VALUES (:uri, :type, :url, :start, :stop)', r.json()['data']['playlist'])
    
    
    con.commit()
    
    for item in r.json()['data']['playlist']:
    	print item['url']
    	urllib.urlretrieve (item['url'], item['uri'])
    #cur.execute('SELECT * from playlist')
    
    #data = cur.fetchone()
    
    #print " %s" % data                
    
except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()