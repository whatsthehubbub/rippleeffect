from fabric.api import *

def install_nginx():
    "install nginx deb package"
    sudo('apt-get install nginx --assume-yes')

def restart_nginx():
    "restart nginx if config is ok"
    sudo('nginx -t')
    sudo('/etc/init.d/nginx restart')
