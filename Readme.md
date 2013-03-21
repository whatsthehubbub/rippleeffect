do a deploy:


* ssh into the server
* git pull
* source venv/bin/activate
* export RIPPLE_PRODUCTION=True
* < do other actions >
* sudo service rippleeffect stop; sudo service rippleeffect start;