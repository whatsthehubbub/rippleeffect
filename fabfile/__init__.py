import os.path
from fabric.api import *
from fabric.colors import cyan

from base import install_base_packages
from nginx import install_nginx
from mysql import install_mysql
from redis import install_redis
from python import install_python, install_virtualenv
from app import (install_app, restart_app, restart_worker,
                 start_worker, stop_worker, is_worker_running,
                 install_requirements)
from supervisor import install_supervisor


env.roledefs = {
    'dev': ['vagrant@127.0.0.1:2222'],
}

# global env settings
env.code_repo = 'git@github.com:whatsthehubbub/rippleeffect.git'
env.project_name = 'rippleeffect'

# default - dev server settings
env.key_filename = os.path.expanduser('~/.vagrant.d/insecure_private_key')
env.host_string  = 'vagrant@127.0.0.1:2222'
env.virtualenv   = '/home/vagrant/venv'
env.home         = '/home/vagrant/rippleeffect'
env.log_home     = '/var/log/rippleeffect'
env.app_user     = 'vagrant'


def virtualenv(command):
    "virtualenv wrapper function"
    return run('source ' + env.virtualenv + '/bin/activate && ' + command)

def git_pull(branch=None):
    with cd(env.home):
        sudo('git pull', user=env.app_user)
        if branch:
            sudo('git checkout %s' % branch, user=env.app_user)
    
@task
def staging():
    """
    Use environment for staging server
    """
    env.key_filename   = os.path.expanduser('~/.ssh/id_rsa.pub')
    env.host_string    = 'deploy@95.138.180.97'
    # app settings
    env.project_domain = 'playrippleeffect.com'
    env.app_user       = 'rippleeffect'
    env.home           = '/var/app/rippleeffect'
    env.log_home       = '/var/log/rippleeffect'
    env.virtualenv     = '/var/env/rippleeffect'


@task
@roles('dev')
def runserver():
    "run django development server"
    # start a background worker
    if is_worker_running() is False:
        print(cyan('starting background worker'))
        start_worker()
    # start the django dev server
    with cd(env.home):
        virtualenv('python manage.py runserver 0.0.0.0:8000')

@task
@roles('dev')
def runworker():
    "run celery worker in the foreground"
    # stop any background workers
    if is_worker_running():
        print(cyan('stopping background worker(s)'))
        stop_worker()
    # start foreground worker
    with cd(env.home):
        virtualenv('python manage.py celery worker --loglevel=INFO')

@task
def shell():
    "run django interactive shell"
    with cd(env.home):
        virtualenv('python manage.py shell')

@task
def syncdb():
    "run django syncdb"
    with cd(env.home):
        virtualenv('python manage.py syncdb')

@task
def migrate():
    "run south migrations"
    with cd(env.home):
        virtualenv('python manage.py migrate')

@task
def deploy(branch='master'):
    """full deploy
    
    checkout latest code (optionally specify branch)
    update app requirements
    reload app server
    reload celery workers
    """
    git_pull(branch)
    install_requirements()
    restart_app()
    restart_worker()

@task
def deploy_soft(branch='master'):
    "checkout latest source, but don't deploy"
    git_pull(branch)

@task
@roles('dev')
def bootstrap():
    "provision local development server"
    local('vagrant up')
    
    install_base_packages()
    # install_nginx()
    install_mysql()
    install_redis()
    install_supervisor()
    install_python()
    install_virtualenv()
    install_app()
