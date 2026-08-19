#!/bin/sh

# Run global alignment on all query sequences and save output

trap "exit \$exit_code" INT TERM
trap "exit_code=\$?; kill \$(jobs -p)" EXIT

for query in queries/*.fa; do
    SECONDS=0
    output=$(echo $query | sed "s/queries/outputs/g; s/query/fasta/g; s/\.fa/\.output/g")
    if [ -s $output ]; then
        if [ $(cat $output | wc -l) -gt 25 ]; then
            echo Output for $query already found, skipping
            continue
        fi
        rm $output
    fi
    echo Aligning to $query
    glsearch36 -s custom.matrix -b 1 -d 1 $query chr1.fna > $output
    echo Finished alignment in $SECONDS seconds to $output
done