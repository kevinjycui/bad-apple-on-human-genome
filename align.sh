#!/bin/sh

# Run global alignment on all query sequences and save output

trap "exit \$exit_code" INT TERM
trap "exit_code=\$?; kill \$(jobs -p)" EXIT

success=0
fail=0
total_time=0
count=0

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

    echo ===
    echo Aligning to $query
    glsearch36 -s custom.matrix -b 1 -d 1 -E 5 $query chr1.fna > $output

    elapsed_time=$SECONDS
    ((total_time += elapsed_time))
    ((count++))

    if [ $(cat $output | wc -l) -gt 25 ]; then
        ((success++))
        echo Succeeded in finding alignment in $elapsed_time seconds to $output
    else
        ((fail++))
        echo Failed to find alignment in $elapsed_time seconds to $output
    fi
    echo Successes: $success,  Fails: $fail
    echo Total time: $total_time, Count: $count, Average time: $((total_time / count))
done