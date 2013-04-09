from fabric.api import *
from fabric.contrib import files

def install_nginx():
    "install nginx deb package"
    sudo('apt-get install nginx=1.1.19-1ubuntu0.1 --assume-yes')

def configure_site():
    "configure an nginx site"
    files.upload_template(
        'nginx/%s.j2' % sitename,
        '/etc/nginx/sites-available/%(project_name)s' % env,
        env,
        template_dir='fabfile/templates',
        use_jinja=True,
        use_sudo=True,
    )
    sudo('ln -s /etc/nginx/sites-available/%(project_name)s /etc/nginx/sites-enabled/%(project_name)s' % env,
         warn_only=True)
    
def restart_nginx():
    "restart nginx if config is ok"
    sudo('service nginx configtest')
    sudo('service nginx restart')

def reload_nginx():
    "reload nginx config"
    sudo('service nginx configtest')
    sudo('service nginx reload')
