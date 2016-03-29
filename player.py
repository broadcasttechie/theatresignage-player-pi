#!/usr/bin/env python
import logging
import sh
from requests import get as req_get
from time import sleep
from json import load as json_load
from signal import signal, SIGUSR1, SIGUSR2
from datetime import datetime, timedelta
from os import path, getenv, utime, environ
from platform import machine
#from settings import settings
import sqlite3 as lite
import copy 

browser = None
current_browser_url = None
HOME = '/home/pi'
arch = None
BLACK_PAGE = "main-viewer.html"
WATCHDOG_PATH = '/tmp/screenly.watchdog'

UZBLRC = 'ts/misc/uzbl.rc'
APP = 'ts'
MEDIA = 'media'
DATABASE = 'player.db'

def sigusr1(signum, frame):
    """
    The signal interrupts sleep() calls, so the currently playing web or image asset is skipped.
    omxplayer is killed to skip any currently playing video assets.
    """
    logging.info('USR1 received, skipping.')
    sh.killall('omxplayer.bin', _ok_code=[1])


def sigusr2(signum, frame):
    """Reload settings"""
    logging.info("USR2 received, reloading settings.")
    #load_settings()



def browser_send(command, cb=lambda _: True):
    if not (browser is None) and browser.process.alive:
        while not browser.process._pipe_queue.empty():  # flush stdout
            browser.next()

        browser.process.stdin.put(command + '\n')
        while True:  # loop until cb returns True
            if cb(browser.next()):
                break
    else:
        logging.info('browser found dead, restarting')
        load_browser()


def load_browser(url=None):
    global browser, current_browser_url
    logging.info('Loading browser...')

    if browser:
        logging.info('killing previous uzbl %s', browser.pid)
        browser.process.kill()

    if url is not None:
        current_browser_url = url

    # --config=-       read commands (and config) from stdin
    # --print-events   print events to stdout
    browser = sh.Command('uzbl-browser')(print_events=True, config='-', uri=current_browser_url, _bg=True)
    logging.info('Browser loading %s. Running as PID %s.', current_browser_url, browser.pid)
    #print ('Browser loading %s. Running as PID %s.', current_browser_url, browser.pid)
    #uzbl_rc = 'set ssl_verify = {}\n'.format('1' if settings['verify_ssl'] else '0')
    uzbl_rc = 'set ssl_verify = 0'
    with open(path.join(HOME, UZBLRC)) as f:
    #with open(HOME + UZBLRC) as f:  # load uzbl.rc
        uzbl_rc = f.read() + uzbl_rc
    browser_send(uzbl_rc)

def browser_send(command, cb=lambda _: True):
    if not (browser is None) and browser.process.alive:
        while not browser.process._pipe_queue.empty():  # flush stdout
            browser.next()

        browser.process.stdin.put(command + '\n')
        while True:  # loop until cb returns True
            if cb(browser.next()):
                break
    else:
        logging.info('browser found dead, restarting')
        load_browser()




def browser_clear(force=False):
    """Load a black page. Default cb waits for the page to load."""
    browser_url('file://' + path.join(HOME, APP, BLACK_PAGEE), force=force, cb=lambda buf: 'LOAD_FINISH' in buf and BLACK_PAGE in buf)


def browser_url(url, cb=lambda _: True, force=False):
    global current_browser_url

    if url == current_browser_url and not force:
        logging.debug('Already showing %s.', current_browser_url)

        # For some reason this invokes a weird black screen issue
        # when going image -> image.
        # logging.debug('Already showing %s, reloading it.', current_browser_url)
        # browser_send('reload full')
    else:
        current_browser_url = url
        browser_send('uri ' + current_browser_url, cb=cb)
        logging.info('current url is %s', current_browser_url)

def view_image(uri):
    browser_clear()
    print(uri)
    browser_send('js window.setimg("{0}")'.format(uri), cb=lambda b: 'COMMAND_EXECUTED' in b and 'setimg' in b)

def browser_clear(force=False):
    """Load a black page. Default cb waits for the page to load.""" 
    #browser_url('file://' + BLACK_PAGE, force=force, cb=lambda buf: 'LOAD_FINISH' in buf and BLACK_PAGE in buf)
    browser_url('file://' + path.join(HOME, APP, BLACK_PAGE), force=force, cb=lambda buf: 'LOAD_FINISH' in buf and BLACK_PAGE in buf)



def dict_gen(curs):
    ''' From Python Essential Reference by David Beazley
    '''
    import itertools
    field_names = [d[0].lower() for d in curs.description]
    while True:
        rows = curs.fetchmany()
        if not rows: return
        for row in rows:
            yield dict(itertools.izip(field_names, row))

def get_playlist():
    #print path.join(HOME, APP, DATABASE)
    con = lite.connect(path.join(HOME, APP, DATABASE))
    con.row_factory = lite.Row
    cur = con.cursor()
    playlist = cur.execute("SELECT * FROM playlist WHERE where DATETIME(start) < DATETIME('now') AND DATETIME(stop) > DATETIME('now')")
    pl = list(playlist)
    if con:
        con.close()
    return pl

def play_playlist(playlist):
    #print playlist
    for row in playlist:
        #print row['duration']
        if 'IMAGE' in row['type']:
            assetfile = path.join(HOME, APP, MEDIA, row['uri'])
            if path.isfile(assetfile):
                view_image(assetfile)
                sleep(row['duration'])
            else:
                sleep(0.5)
        else if 'VIDEO' in row['type']:
        	print 'Video'
        else:
            sleep(0.5)


def setup():
    global HOME, arch, db_conn
    HOME = getenv('HOME', '/home/pi/')
    environ['DISPLAY'] = ':0'
    arch = machine()
    print HOME
    signal(SIGUSR1, sigusr1)
    signal(SIGUSR2, sigusr2)

    #load_settings()
    #db_conn = db.conn(settings['database'])

    #sh.mkdir(SCREENLY_HTML, p=True)
    #html_templates.black_page(BLACK_PAGE)




def main():
    print "Starting"
    setup()
    #get_playlist()
    #url = 'http://{0}:{1}/splash_page'.format(settings.get_listen_ip(), settings.get_listen_port()) if settings['show_splash'] else 'file://' + BLACK_PAGE
    url = BLACK_PAGE
    load_browser(url=url)
    #if settings['show_splash']:
    #    sleep(SPLASH_DELAY)

    #scheduler = Scheduler()
    logging.debug('Entering infinite loop.')
    #browser_url('http://ts.zamia.co.uk/playlist/2/player')
    while True:
        #asset_loop(scheduler)
        pl = get_playlist()
        play_playlist(pl)
        #mediaroot =  path.join(HOME , APP, MEDIA)
        #delay = 5
        #sleep(3)
        #view_image(mediaroot + 'greatex2-1080.jpg')
        #sleep(delay)
        #view_image(mediaroot + 'twelfth2-1080.jpg')
        #sleep(delay)
        #view_image(mediaroot + 'grimm-1080.jpg')
        #sleep(delay)
        #view_image(mediaroot + 'twelfth2-final1C_150rgb.jpg')
        #browser_url('http://bbc.co.uk/news')
        #sleep(delay)
        #browser_url('http://bbc.co.uk/cbbc')
        #sleep(delay)


if __name__ == "__main__":
    try:
        main()
    except:
        logging.exception("Viewer crashed.")
        raise


