#!/bin/bash

# Filename to store ticket IDs in
ftickets=$1
# Input directory. Must have `.fa` files ONLY.
input_dir=$2

# The batch query in Genesearch queues up an alignment search for a query sequence
# against a specific namespace, and return a ticket number that can be used to
# retrieve the results upon completion.
# You can use a batch search for a query that you expect to take a long time.
# ID	The unique identifier for the namespace to search for alignments
# Query Parameters:
# 1) file	    | A FASTA file containing query sequences for which alignments are
#               sought in the given namespace
# 2) sequence	| A string containing a query sequence (as an alternative to file)
# 3) eVal	    | The maximum E-Value threshold for the search (default: none)
# 4) maxHits	| The number of results after which the search immediately returns
#               (default: no max)
# Returns a ticket number that can be used to retrieve results upon completion.

cat /dev/null >$ftickets
for fs in $input_dir/*; do
  curl --silent \
    -F file=@$fs \
    https://genesearch.kbase.us/namespace/uniref90/batch >>$ftickets
  name=$(basename -- "$fs")
  name="${name%.*}"
  echo -e "\t$name" >>$ftickets
  sleep 3
done
