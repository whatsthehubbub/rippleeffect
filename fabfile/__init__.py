import os.path
from fabric.api import *
from fabric.colors import cyan

from base import install_base_packages
from nginx import install_nginx
from mysql import install_mysql
from redis import install_redis
from python import install_python, install_virtualenv
from app import install_app, start_worker, stop_worker, is_worker_running
from supervisor import install_supervisor


env.roledefs = {
    'dev': ['vagrant@127.0.0.1:2222'],
}
# add vagrant keyfile
env.key_filename = os.path.expanduser('~/.vagrant.d/insecure_private_key')
env.virtualenv   = '/home/vagrant/venv'
env.home         = '/home/vagrant/rippleeffect'
env.project_name = 'rippleeffect'
env.project_home = os.path.join(env.home, env.project_name)
env.log_home     = os.path.join('/var/log/', env.project_name)
env.app_user     = 'vagrant'

def virtualenv(command):
    "virtualenv wrapper function"
    return run('source ' + env.virtualenv + '/bin/activate && ' + command)

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
        virtualenv('python manage.py celery worker --loglevel=INFO -B')

@task
@roles('dev')
def shell():
    "run django interactive shell"
    with cd(env.home):
        virtualenv('python manage.py shell')

@task
@roles('dev')
def syncdb():
    "run django syncdb"
    with cd(env.home):
        virtualenv('python manage.py syncdb')

@task
@roles('dev')
def migrate():
    "run south migrations"
    with cd(env.home):
        virtualenv('python manage.py migrate')

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
