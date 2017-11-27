import sys
import argparse
import kivo
from .logging import log
from .command import resolve
from .util.io import slurp_json
from .util.argparse import splitargv
from .decorators import timedsingle

TRACE = False # for noisy exception tracing

def configure():
    log.debug('..')
    kivo.module.build_index()
    kivo.pgconf = slurp_json("config/postgres.json")

USAGE = """etl command [arguments] [<keyword-arguments>]"""
def parse_options(kwargv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", type=str, required=False, help="staging root", default='stage')
    parser.add_argument("--debug", required=False, action="store_true", help="more debugging")
    parser.add_argument("--trace", required=False, action="store_true", help="show noisy exception traces")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--module", type=str, help="module name")
    group.add_argument("--table", type=str, help="table name")
    return parser.parse_args(kwargv)

def parse_args():
    posargv,kwargv = splitargv(sys.argv[1:])
    command = posargv[0] if len(posargv) else None
    posargs = posargv[1:]
    options = parse_options(kwargv)
    return command,posargs,options

@timedsingle
def dispatch(command,posargs,options=None):
    log.debug("command='%s', posargs=%s, options=%s" % (command,posargs,options))
    log.info("%s %s .." % (command,posargs))
    if command is None:
        log.error("no command argument")
        return False
    handler = resolve(command)
    if handler:
        try:
            return handler(posargs,options)
        except (ValueError, RuntimeError) as e:
            if TRACE:
                log.exception(e)
            log.error(str(e))
            return False
    else:
        log.error("unrecognized command '%s'" % command)
        return False

def main():
    global TRACE
    command,posargs,options = parse_args()
    log.debug(f'posargs = {posargs}')
    log.debug(f'options = {options}')
    if options.debug:
        kivo.logging.setlevel(log,'debug')
    if options.trace:
        TRACE = True
    configure()
    status,delta = dispatch(command,posargs,options)
    _status = 'OK' if status else 'FAILED'
    log.info("status = %s in %.3f sec" % (_status,delta))
    log.info("done")

if __name__ == '__main__':
    main()


