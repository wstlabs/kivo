#!/usr/bin/env python3.6
#
# A simple argument packer for the standard psql client. 
# Assumes we'll be using the 'writeuser', whose password has been
# set in the default .pgpass location (per the setup instructions). 
#
# TODO: explain args + volatility
#
import os
import sys
import simplejson as json
from subprocess import call

APPROOT = os.environ.get('DWXROOT')
if APPROOT is None:
    raise RuntimeError("bad environment setup - no DWROOT variable set")

pgargs = sys.argv[1:]

configpath = f"{APPROOT}/config/postgres.json"
pgconf = json.loads(open(configpath,"r").read())
hostname = pgconf.get('hostname')

# print("pgconf = ",pgconf)
# print("pgargs = ",pgargs)

hostflag = " -h %s" % hostname if hostname else ''
flags = "-U %(user)s -d %(dbname)s " % pgconf
flags += hostflag

command = "psql %s %s" % (flags,' '.join(pgargs))
print("EXEC: %s" % command)
call(command,shell=True)

