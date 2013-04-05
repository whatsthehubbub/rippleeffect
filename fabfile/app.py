from fabric.api import *
from fabric.contrib import files
from .nginx import configure_site, reload_nginx
from .supervisor import restart_supervisor

packages = (
    'libmysqlclient-dev=5.5.29-0ubuntu0.12.04.2',
)


def install_app():
    create_app_user()
    prepare_directories()
    prepare_virtualenv()
    install_requirements()
    configure_site()
    configure_workers()

def create_app_user():
    if files.contains('/etc/passwd',env.app_user):
        return
    
    sudo('useradd %(app_user)s --create-home --shell /bin/bash' % env)
    
    # let deploy user switch to app_user without password
    sudo_line = 'deploy  ALL=(%(app_user)s) NOPASSWD: ALL' % env
    if not files.contains('/etc/sudoers', sudo_line):
        files.append('/etc/sudoers', sudo_line, use_sudo=True)
    
    # update the app user's ssh config
    files.upload_template(
        'ssh/config',
        '/home/%(app_user)s/.ssh/config' % env,
        env,
        template_dir='fabfile/templates',
        use_sudo=True,
        mode=644,
    )
    sudo('chown %(app_user)s:%(app_user)s /home/%(app_user)s/.ssh/config' % env)
    
    # update the app user's ssh known_hosts
    files.upload_template(
        'ssh/config',
        '/home/%(app_user)s/.ssh/known_hosts' % env,
        env,
        template_dir='fabfile/templates',
        use_sudo=True,
        mode=644,
    )
    sudo('chown %(app_user)s:%(app_user)s /home/%(app_user)s/.ssh/known_hosts' % env)

def virtualenv(command, user=None):
    if user:
        return sudo('source ' + env.virtualenv + '/bin/activate && '+command, user=user)
    else:
        return run('source ' + env.virtualenv + '/bin/activate && ' + command)

def prepare_virtualenv():
    "installs app's virtualenv"
    if not files.exists(env.virtualenv):
        _prepare_dir(env.virtualenv)
        sudo('virtualenv %(virtualenv)s --distribute' % env, user=env.app_user)

def _prepare_dir(directory):
    user = env.app_user
    if run('test -d %(directory)s' % locals(), warn_only=True).failed:
        sudo('mkdir -p %(directory)s' % locals())
        sudo('chown %(user)s:%(user)s %(directory)s' % locals())
        sudo('chmod 755 %(directory)s' % locals())

def prepare_directories():
    "creates, chmod's, chown's required directories"
    # prepare home directory
    _prepare_dir(env.home)
    # prepare logging directory
    _prepare_dir(env.log_home)
    # prepare celerybeat-schedule directory
    _prepare_dir('/var/lib/celery')

def clone_repo():
    "do the initial git clone"
    with cd(env.home), cd('..'):
        sudo('git clone %(code_repo)s' % env,user=env.app_user)

@task
def install_requirements():
    "installs app's required packages"
    for package in packages:
        sudo('apt-get install %s --assume-yes' % package)
    
    with cd(env.home):
        for line in open('requirements.txt','r'):
            virtualenv('pip install %s' % line, user=env.app_user)


def configure_app():
    "configure app server"
    files.upload_template(
        'supervisor/rippleeffect.conf.j2',
        '/etc/supervisor/conf.d/rippleeffect.conf',
        env,
        template_dir='fabfile/templates',
        use_jinja=True,
        use_sudo=True,
    )


def configure_workers():
    "configure celery workers"
    # upload supervisord config for celery worker
    files.upload_template(
        'supervisor/celery.conf.j2',
        '/etc/supervisor/conf.d/celery.conf',
        env,
        template_dir='fabfile/templates',
        use_jinja=True,
        use_sudo=True,
    )
    # upload supervisord config for celerybeat
    files.upload_template(
        'supervisor/celerybeat.conf.j2',
        '/etc/supervisor/conf.d/celerybeat.conf',
        env,
        template_dir='fabfile/templates',
        use_jinja=True,
        use_sudo=True,
    )
    restart_supervisor()

@task
def start():
    "start rippleeffect uwsgi app"
    sudo('supervisorctl start rippleeffect')

@task
def stop():
    "stop rippleeffect uwsgi app"
    sudo('supervisorctl stop rippleeffect')

@task
def restart():
    "restart rippleeffect uwsgi app"
    sudo('supervisorctl restart rippleeffect')

restart_app = restart

def start_worker():
    "start celery background worker"
    sudo('supervisorctl start celery')

def stop_worker():
    "stop celery background worker"
    sudo('supervisorctl stop celery')

def restart_worker():
    "restart celery background worker"
    sudo('supervisorctl restart celery')

def is_worker_running():
    "indicates if a celery worker is running"
    res = run('pgrep -fl "[c]elery\s" | wc -l')
    return int(res) > 0

