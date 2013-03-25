from time import sleep
from fabric.api import *

def install_supervisor():
    "install supervisord via pip"
    sudo('apt-get install supervisor=3.0a8-1.1 --assume-yes')

def start_supervisor():
    "start supervisord"
    sudo('service supervisor start')

def stop_supervisor():
    "stop supervisor"
    sudo('service supervisor stop')

def restart_supervisor():
    "restart supervisor"
    stop_supervisor()
    sleep(3) # supervisor needs a little time to shutdown, but doesn't block
    start_supervisor()
