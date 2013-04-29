from fabric.api import *
from fabric.colors import cyan
from fabric.contrib import files

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


def upgrade_system():
    sudo('apt-get update')
    sudo('apt-get dist-upgrade --assume-yes --quiet')
    

def create_deploy_user():
    "creates deployment user"
    username = 'deploy'
    # create deploy user & home without password
    if files.contains('/etc/passwd', username):
        return
    
    sudo('useradd %s --create-home --shell /bin/bash' % username)

    # create authorized_keys & upload public key
    sudo('mkdir -p /home/deploy/.ssh')
    sudo('chmod 700 /home/deploy/.ssh')
    pub_key = open(env.key_filename, 'rb').read()
    files.append('/home/%s/.ssh/authorized_keys' % username, pub_key, use_sudo=True)

    # update authorized_keys permissions
    sudo('chmod 400 /home/%s/.ssh/authorized_keys' % username)
    sudo('chown deploy:deploy /home/%s/.ssh -R' % username)

    # create sudo password & add to sudoers
    print(cyan('set sudo password for "%s" user' % username))
    sudo('passwd %s' % username)
    files.append('/etc/sudoers', '%s  ALL=(ALL) ALL' % username, use_sudo=True)


def automate_security_updates():
    "enable automatic installation of security updates"
    sudo('apt-get install unattended-upgrades')
    files.upload_template(
        'apt/10periodic',
        '/etc/apt/apt.conf.d/10periodic',
        env,
        template_dir='fabfile/templates',
        use_sudo=True,
        mode=644,
    )
    # TODO: checkout apticron for email alerts


def install_rackspace_monitoring():
    # add the rackspace apt repo to list
    files.append("/etc/apt/sources.list.d/rackspace-monitoring-agent.list",
        "deb http://stable.packages.cloudmonitoring.rackspace.com/ubuntu-12.04-x86_64 cloudmonitoring main",
        use_sudo=True)
    # install rackspace repo signing key
    run('curl https://monitoring.api.rackspacecloud.com/pki/agent/linux.asc | apt-key add -')
    # install the monitoring agent
    run('apt-get update')
    run('apt-get install rackspace-monitoring-agent')
    # run setup
    run('rackspace-monitoring-agent --setup')


def harden_sudoers():
    """
    >> /etc/sudoers
    root    ALL=(ALL) ALL
    deploy  ALL=(ALL) ALL
    """
    pass


def harden_ssh():
    """
    >> /etc/ssh/sshd_config
    PermitRootLogin no
    PasswordAuthentication no
    """
    run('service ssh restart')


def setup_firewall():
    """
    ufw allow from {your-ip} to any port 22
    ufw allow 80
    ufw enable
    """
    pass


def harden_server():
    setup_firewall()
    harden_ssh()
    harden_sudoers()


def provision_base_server():
    upgrade_system()
    install_base_packages()
    automate_security_updates()
    create_deploy_user()
