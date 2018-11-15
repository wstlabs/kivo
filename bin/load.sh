#!/bin/sh
#
# A trivial wrapper for the 'load' app.
#

die () {
    echo >&2 "$@"
    exit 1
}

check_args () {
    [ "$#" -eq 1 ] || die "1 argument required, $# provided"
    echo $1 | grep -E -q '^[A-Za-z0-9\-]+$' || die "dash-case argument required at position 1, $1 provided"
}

check_args $@
source=$1
python3.6 -m kivo.app.load --source=$source

