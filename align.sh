#!/bin/sh

trap "exit \$exit_code" INT TERM
trap "exit_code=\$?; kill \$(jobs -p)" EXIT

for query in queries/*.fa; do
    output="outputs/$query.output"
    if [ -s $output ]; then
        if [ $(cat $output | wc -l) -gt 15 ]; then
            echo Output for $query already found, skipping
            continue
        fi
        rm $output
    fi
    echo Aligning to $query
    (glsearch36 -s custom.matrix $query chr1.fna > $output && echo Done aligning to $query) &
    while [ $(jobs -rp | wc -l) -ge 3 ]; do
        sleep 1
    done
done