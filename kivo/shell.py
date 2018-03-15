from subprocess import call
from .logging import log

def invoke(command):
    log.debug("command = [%s]" % command)
    status = call(command,shell=True)
    log.debug("status = %s" % status)
    return status == 0

def make_psql_command(statement,pgconf):
    quoted = '"'+statement+'"'
    hostname = pgconf.get('hostname')
    hostflag = " -h %s" % hostname if hostname else ''
    flags = "-U %(user)s -d %(dbname)s" % pgconf
    flags += hostflag
    return "psql %s -c %s" % (flags,quoted)

def dopsql(statement,pgconf):
    command = make_psql_command(statement,pgconf)
    log.debug("command = [%s]" % command)
    return invoke(command)

