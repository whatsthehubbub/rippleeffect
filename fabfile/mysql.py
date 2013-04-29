from fabric.api import *

MYSQL_ROOT_PASSWORD = env.get('mysql-root-password','root')

def install_mysql():
    "install mysql server and mysql client library headers"
    
    if run('which mysql', warn_only=True).succeeded:
        return
    
    # set the password to avoid interactive package config
    sudo("debconf-set-selections <<< 'mysql-server-5.5.29-0ubuntu0.12.04.2 mysql-server/root_password password %s'" % MYSQL_ROOT_PASSWORD)
    sudo("debconf-set-selections <<< 'mysql-server-5.5.29-0ubuntu0.12.04.2 mysql-server/root_password_again password %s'" % MYSQL_ROOT_PASSWORD)
    # do the actual installation
    sudo('apt-get install mysql-server=5.5.29-0ubuntu0.12.04.2 '
         'libmysqlclient-dev=5.5.29-0ubuntu0.12.04.2 '
         '--assume-yes')

def configure_mysql():
    "configure mysql server"
    execute_query("CREATE DATABASE hubub;")
    execute_query("GRANT ALL ON hubbub.* TO hubbub@localhost IDENTIFIED BY 'hubbub';")
    execute_query("FLUSH PRIVILEGES;")

def execute_query(query):
    "execute mysql query"
    return run('mysql -uroot -proot -e "%s"' % query)

def start_mysql():
    "start mysql server"
    sudo('service mysql start')

def stop_mysql():
    "stop mysql server"
    sudo('service mysql stop')
