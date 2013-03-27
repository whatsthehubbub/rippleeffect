from fabric.api import *


packages = (
    'build-essential',
    'git',
    'mercurial',
    'rsync',
    'vim',
)

def install_base_packages():
    sudo('apt-get update')
    for package in packages:
        sudo('apt-get install %s --assume-yes' % package)
