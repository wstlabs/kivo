#!/bin/sh
#
# A trivial wrapper for the 'pull' app.
#

die () {
    echo >&2 "$@"
    exit 1
}

check_args () {
    [ "$#" -eq 2 ] || die "2 arguments required, $# provided"
    echo $1 | grep -E -q '^[A-Za-z0-9\-]+$' || die "dash-case argument required at position 1, $1 provided"
    echo $2 | grep -E -q '^[A-Za-z0-9\-]+$' || die "dash-case argument required at position 2, $2 provided"
}

check_args $@
source=$1
version=$2
python3.6 -m kivo.app.pull --name=$source --month=$version

