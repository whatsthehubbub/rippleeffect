from fabric.api import *

def install_python():
    "install python deb package"
    sudo('apt-get install python=2.7.3-0ubuntu2 python-dev=2.7.3-0ubuntu2 --assume-yes')

def install_virtualenv():
    "install virtualenv from source"
    # because ubuntu's python-virtualenv is out of date
    version = '1.9.1'
    package = 'virtualenv-%s' % version
    
    # skip if this version is already installed
    if run('which virtualenv', warn_only=True).succeeded:
        if run('virtualenv --version') == version:
            return
        
    with cd('/tmp'):
        run('wget https://pypi.python.org/packages/source/v/virtualenv/%s.tar.gz' % package)
        run('tar xvfz %s.tar.gz' % package)
        with cd(package):
            sudo('python setup.py install')
