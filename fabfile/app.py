from fabric.api import *
from fabric.contrib.files import exists, upload_template
from .supervisor import restart_supervisor

def install_app():
    prepare_directories()
    prepare_virtualenv()
    install_requirements()
    configure_workers()

def virtualenv(command):
    return run('source ' + env.virtualenv + '/bin/activate && ' + command)

def prepare_virtualenv():
    "installs app's virtualenv"
    if not exists(env.virtualenv):
        run('virtualenv %(virtualenv)s --distribute' % env)

def prepare_directories():
    "creates, chmod's, chown's required directories"
    if run('test -d %(log_home)s' % env, warn_only=True).failed:
        sudo('mkdir -p %(log_home)s' % env)
        sudo('chown %(app_user)s:%(app_user)s %(log_home)s' % env)
        sudo('chmod 755 %(log_home)s' % env)

def install_requirements():
    "installs app's required packages"
    with cd(env.home):
        virtualenv('pip install -r requirements.txt')

def configure_workers():
    "configure celery workers"
    # upload supervisord config for celery worker
    upload_template(
        'celery.conf.j2',
        '/etc/supervisor/conf.d/celery.conf',
        env,
        template_dir='fabfile/templates',
        use_jinja=True,
        use_sudo=True,
    )
    # upload supervisord config for celerybeat
    upload_template(
        'celerybeat.conf.j2',
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
    res = run('pgrep -fl [c]elery | wc -l')
    return int(res) > 0

