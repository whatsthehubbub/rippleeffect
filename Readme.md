Dev Environment Setup
=====================
1. Download and install [VirtualBox for OSX](http://download.virtualbox.org/virtualbox/4.2.10/VirtualBox-4.2.10-84104-OSX.dmg)
2. Download and install [vagrant for OSX](http://files.vagrantup.com/packages/67bd4d30f7dbefa7c0abc643599f0244986c38c8/Vagrant.dmg)
3. Install [fabric](http://docs.fabfile.org) and Jinja `sudo pip install --upgrade fabric==1.6.0 jinja2`
4. Checkout the repository `git clone git@github.com:whatsthehubbub/rippleeffect.git && cd rippleeffect`
5. Bootstrap the dev environment `fab bootstrap` (you may want to grab a coffee)

Dev Environment Usage
=====================
Your dev environment runs a VirtualBox instance where the checkout you just did is mapped into. Any files you change on your machine are mirrored into the virtual machine and vice versa. The dev server runs on the virtual machine and forwards its ports to your local machine.

You can interface with your VM using the [vagrant](http://docs.vagrantup.com/v2/getting-started/index.html) command. The commands you'll most often use are `vagrant up` and `vagrant halt`.

To be up and running do this:

* git pull
* vagrant up
* fab syncdb (only once on every new database)
* fab migrate (only when the database schema has been changed)
* fab app.install_requirements (only when new packages have been added)
* fab runserver;
* Access your environment at: http://127.0.0.1:8000

This process does not create a superuser. To create one:
* fab shell;
* from riskgame.models import EmailUser
* EmailUser.objects.create_superuser('admin@email.com', 'admin')

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


Tech Trial Deployment
=====================

* ssh into the server
* git pull
* source venv/bin/activate
* export RIPPLE_PRODUCTION=True
* < do other actions >
* sudo service rippleeffect stop; sudo service rippleeffect start;
