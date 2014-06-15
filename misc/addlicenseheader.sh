#!/bin/bash

CMDDIR=$(dirname ${0})

LHEADER="$(echo "$(cat $CMDDIR/licenseheader.txt)" | sed -r "s/$/NEWLINE/g" | tr -d '\n')"
sed -i "s|^# TBD:LICENSE|$LHEADER|" $@
sed -i "s/NEWLINE/\n/g" $@

