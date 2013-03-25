do a deploy:


* ssh into the server
* git pull
* source venv/bin/activate
* export RIPPLE_PRODUCTION=True
* < do other actions >
* sudo service rippleeffect stop; sudo service rippleeffect start;

Dev Environment Setup
=====================
1. Download and install [VirtualBox for OSX](http://download.virtualbox.org/virtualbox/4.2.10/VirtualBox-4.2.10-84104-OSX.dmg)
2. Download and install [vagrant for OSX](http://files.vagrantup.com/packages/f743fed3cc0466839a97d4724ec0995139f87806/Vagrant.dmg)
3. Install [fabric](http://docs.fabfile.org) `sudo pip install fabric`
4. Checkout the repository `git clone git@github.com:whatsthehubbub/rippleeffect.git && cd rippleeffect`
5. Bootstrap the dev environment `fab bootstrap` (you may want to grab a coffee)

Dev Environment Usage
=====================
Your dev environment runs a VirtualBox instance. You can interface with your VM using the [vagrant](http://docs.vagrantup.com/v2/getting-started/index.html) command. The commands you'll most often use are `vagrant up` and `vagrant halt`.

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
