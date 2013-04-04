from fabric.api import *
from fabric.contrib import files
from .supervisor import restart_supervisor

packages = (
    'libmysqlclient-dev=5.5.29-0ubuntu0.12.04.2',
    'uwsgi=1.0.3+dfsg-1ubuntu0.1',
    'uwsgi-plugin-python=1.0.3+dfsg-1ubuntu0.1',
)

def install_app():
    create_app_user()
    prepare_directories()
    prepare_virtualenv()
    install_requirements()
    configure_workers()

def create_app_user():
    if files.contains('/etc/passwd',env.app_user):
        return
    
    sudo('useradd %(app_user)s --create-home --shell /bin/bash' % env)
    
    # let deploy user switch to app_user without password
    sudo_line = 'deploy  ALL=(%(app_user)s) NOPASSWD: ALL' % env
    if not files.contains('/etc/sudoers', sudo_line):
        files.append('/etc/sudoers', sudo_line, use_sudo=True)

def virtualenv(command, user=None):
    if user:
        return sudo('source ' + env.virtualenv + '/bin/activate && '+command, user=user)
    else:
        return run('source ' + env.virtualenv + '/bin/activate && ' + command)

def prepare_virtualenv():
    "installs app's virtualenv"
    if not exists(env.virtualenv):
        sudo('virtualenv %(virtualenv)s --distribute' % env)

def prepare_directories():
    "creates, chmod's, chown's required directories"
    # prepare home directory
    if run('test -d %(home)s' % env, warn_only=True).failed:
        sudo('mkdir -p %(home)s' % env)
        sudo('chown %(app_user)s:%(app_user)s %(home)s' % env)
        sudo('chmod 755 %(home)s' % env)
    
    # prepare logging directory
    if run('test -d %(log_home)s' % env, warn_only=True).failed:
        sudo('mkdir -p %(log_home)s' % env)
        sudo('chown %(app_user)s:%(app_user)s %(log_home)s' % env)
        sudo('chmod 755 %(log_home)s' % env)
    
    # prepare celerybeat-schedule directory
    celery_dir = '/var/lib/celery'
    if run('test -d %s' % celery_dir, warn_only=True).failed:
        sudo('mkdir %s -p ' % celery_dir)
        sudo('chown %(app_user)s:%(app_user)s %(dir)s' % {
            'dir': celery_dir,
            'app_user': env.app_user,
        })
        sudo('chmod 755 %s' % celery_dir)

@task
@roles('dev')
def install_requirements():
    "installs app's required packages"
    for package in packages:
        sudo('apt-get install %s --assume-yes' % package)
    
    with cd(env.home):
        for line in open('requirements.txt','r'):
            virtualenv('pip install %s' % line)

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

def start_worker():
    "start celery background worker"
    sudo('supervisorctl start celery')

def stop_worker():
    "stop celery background worker"
    sudo('supervisorctl stop celery')

def is_worker_running():
    "indicates if a celery worker is running"
    res = run('pgrep -fl "[c]elery\s" | wc -l')
    return int(res) > 0

