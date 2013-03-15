#!/bin/bash
set -e

PROJDIR=/home/alper/rippleeffect

LOGFILE=$PROJDIR/log/gunicorn.log
LOGDIR=$(dirname $LOGFILE)

export RIPPLE_PRODUCTION=True

NUM_WORKERS=3

# user/group to run as
USER=alper
GROUP=alper

cd $PROJDIR
source venv/bin/activate

test -d $LOGDIR || mkdir -p $LOGDIR

exec venv/bin/gunicorn_django -w $NUM_WORKERS \
--user=$USER --group=$GROUP --log-level=debug \
--log-file=$LOGFILE 2>>$LOGFILE
