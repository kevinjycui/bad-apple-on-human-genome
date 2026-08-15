#!/bin/sh

# Run global alignment on all query sequences and save output

trap "exit \$exit_code" INT TERM
trap "exit_code=\$?; kill \$(jobs -p)" EXIT

for query in queries/*.fa; do
    output=$(echo $query | sed "s/queries/outputs/g; s/query/fasta/g; s/\.fa/\.output/g")
    if [ -s $output ]; then
        if [ $(cat $output | wc -l) -gt 15 ]; then
            echo Output for $query already found, skipping
            continue
        fi
        rm $output
    fi
    echo Aligning to $query
    glsearch36 -s custom.matrix $query chr1.fna > $output
done