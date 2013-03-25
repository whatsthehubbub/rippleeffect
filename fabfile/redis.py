from fabric.api import *

def install_redis():
    "install redis server from deb package"
    sudo('apt-get install redis-server=2:2.2.12-1build1 --assume-yes')

def start_redis():
    "start redis server"
    sudo('service redis-server start')

def stop_redis():
    "stop redis server"
    sudo('service redis-server stop')
