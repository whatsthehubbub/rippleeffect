# Ripple Effect

For more details on Ripple Effect see: http://whatsthehubbub.nl/projects/ripple-effect/

Ripple Effect is released under a MIT License as detailed in the LICENSE file in this same directory.

Dev Environment Setup
=====================
1. Download and install [VirtualBox for OSX](http://download.virtualbox.org/virtualbox/4.2.10/VirtualBox-4.2.10-84104-OSX.dmg)
2. Download and install [vagrant for OSX](http://files.vagrantup.com/packages/67bd4d30f7dbefa7c0abc643599f0244986c38c8/Vagrant.dmg)
3. Get the "Command Line Tools for Xcode":https://developer.apple.com/downloads or "Xcode":http://itunes.apple.com/us/app/xcode/id497799835
3. Install [fabric](http://docs.fabfile.org) and Jinja `sudo pip install --upgrade fabric==1.6.0 jinja2`
4. Checkout the repository `git clone git@github.com:whatsthehubbub/rippleeffect.git && cd rippleeffect`
5. Bootstrap the dev environment `fab bootstrap` (you may want to grab a coffee)

Dev Environment Usage
=====================
Your dev environment runs a VirtualBox instance where the checkout you just did is mapped into. Any files you change on your machine are mirrored into the virtual machine and vice versa. The dev server runs on the virtual machine and forwards its ports to your local machine.

You can interface with your VM using the [vagrant](http://docs.vagrantup.com/v2/getting-started/index.html) command. The commands you'll most often use are `vagrant up` and `vagrant halt`.

To be up and running do this:

* git pull (or sync in your Github.app)
* git checkout develop (we work in branch develop)
* vagrant up
* fab app.install_requirements (only when new packages have been added)
* fab syncdb (only once on every new database)
* fab migrate (only when the database schema has been changed)
* fab runserver;
* Access your environment at: http://127.0.0.1:8000

* You can impersonate other players by adding ?impersonate=admin@email.com behind a URL if you're logged in. You can stop by adding ?unimpersonate=1

* Kill the VM with: vagrant halt

This process does not create a superuser. To create one:
* fab shell;
* from riskgame.models import EmailUser
* EmailUser.objects.create_superuser('admin@email.com', 'password')

When you're done stop your virtual machine with `vagrant halt` though you shouldn't really notice it and it will disappear on next reboot.


To get a list of available commands

	fab -l

To run your django dev server:

	fab runserver	# serves django app on localhost:8000

To sync your DB:

	fab syncdb

To run a DB migration

	fab migrate

To run a celery worker in the foreground

	fab runworker

To run a django interactive shell

	fab shell

To shutdown your virtual machine

	vagrant halt

To startup your virtual machine

	vagrant up

To drop into a shell on your virtual machine

	vagrant ssh

The vagrant commands should be executed in the directory which contains the `Vagrantfile`


Staging Deployment
==================
To view a full list of available commands:

    fab --list

To deploy simple app updates:

    fab staging deploy  # deploy the master branch to staging
        
To deploy more complex updates:

    fab staging git_pull migrate reload  # pull code, run migrations, reload app in staging
    
    # pull release branch, install requirements & reload app in staging
    fab staging git_pull:release app.install_requirements migrate collectstatic reload

To tail the application logs:
    
    fab staging logs    # tail the staging app log
    fab staging logs:nginx  # tail the staging webserver log
    fab staging logs:celery # tail the celery worker log
    fab --display logs  # for more information

Do partial updates
==================

To update nginx:

    from fabfile import staging
    from fabfile.nginx import configure_site, restart_nginx
    staging()
    configure_site()
    restart_nginx()

To enable automatic security updates:

    from fabfile import staging
    from fabfile.base import automate_security_updates
    staging()
    automate_security_updates()

Everything runs as rippleeffect, so `sudo -i -u rippleeffect`

Production Deployment
=====================
To spinup a new server:

1. In the [control panel](https://mycloud.rackspace.co.uk/a/alper/#new), create a new server from the saved image `appserver`.
2. Deploy the latest code to the server: `fab prod deploy deploy@<ip-address>`
3. In the [control panel](https://mycloud.rackspace.co.uk/a/alper/load_balancers#rax%3Aload-balancer%2CcloudLoadBalancers%2CLON/60541), add the server to the load balancer.


Tech Trial Deployment
=====================

* ssh into the server
* git pull
* source venv/bin/activate
* export RIPPLE_PRODUCTION=True
* < do other actions >
* sudo service rippleeffect stop; sudo service rippleeffect start;

Branches
========

* develop is mainline development
* release is the version currently on playrippleeffect.com
* master is currently unused

Editing CSS and Javascript
==========================

CSS is written in SCSS, Javascript is written in Coffeescript. It's important to only edit
the .scss and .coffee source files, otherwise your changes will be lost on a subsequent
compile. The easiest way to compile these files on your local machine is to use
Fire.app (http://fireapp.handlino.com/) and watch the 'static' folder (be sure to issue a
'clean and compile' when you add a new file, otherwise it won't be seen).

Setting up your Vista/IE8 image
===============================

To be able to access your local host from the virtual machine, you'll need to add a host-only network:

* Open your VirtualBox preferences
* Go to Network
* This is probably empty, [click to add a new one](https://dl.dropbox.com/s/zmru0yh2y9vlqj9/2013-04-08_at_17.56.50.png)
* Then, open the newly added network's settings and [note down the IP address](https://dl.dropbox.com/s/qx9y4p865tnpdya/2013-04-08_at_17.58.01.png)
* Close these settings and open the settings of the virtual machine. Go to network again. Adapter 1 should be set NAT. [Make sure Adapter 2 is set to the host-only adapter you just created](https://dl.dropbox.com/s/od48vxbl90jp5wf/2013-04-08_at_18.00.09.png). 
* Now, launch your image. Open the windows explorer and [navigate to Windows\System32\drivers\etc](https://dl.dropbox.com/s/9xnels3daeak2la/2013-04-08_at_18.05.45.png) and open the hosts file with Notepad.
* Make sure the IP address pointing to local hosts [is the one you noted down earlier](https://dl.dropbox.com/s/c5az3cukdhm5e2c/2013-04-08_at_18.06.23%20%281%29.png).
* Save the file, launch Internet Explorer and [open your locally running Ripple Effect website](https://dl.dropbox.com/s/tfwd0iapolxsmn4/2013-04-08_at_18.07.22.png) through the same IP address with :8000 appended.
