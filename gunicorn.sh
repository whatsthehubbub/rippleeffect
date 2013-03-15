#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/hello.log
LOGDIR=$(dirname $LOGFILE)

NUM_WORKERS=3

# user/group to run as
USER=alper
GROUP=alper

cd /home/alper/rippleeffect
source venv/bin/activate

test -d $LOGDIR || mkdir -p $LOGDIR

exec venv/bin/gunicorn_django -w $NUM_WORKERS \
--user=$USER --group=$GROUP --log-level=debug \
--log-file=$LOGFILE 2>>$LOGFILE