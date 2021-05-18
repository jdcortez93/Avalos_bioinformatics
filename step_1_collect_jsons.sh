#!/bin/bash

# location of JSON dumps
json_dumps="json_dumps/"
mkdir -p $json_dumps

# Filename for storing ticket information
# Iterate over the lines from this file going over ticket by ticket
ftickets=$1

while IFS= read -r line
do
    # check if blank
    if [ -z "$line" ]; then
        continue
    fi
    line=$(echo -e "$line" | cut -d$'\t' -f1)
    # "Get All Tickets" endpoint retrieves status information for all tickets corresponding
    # to batch alignment searches. Each ticket can be "queued", "processing", or "completed".
    # Example: { "11":"completed", "12":"completed", "13":"completed", "14":"completed", "15":"processing",
    # "16":"processing", "17":"processing", "18":"queued" }
    status=""
    while [ "$status" != "completed" ]; do
        status=$(curl --silent \
            'https://genesearch.kbase.us/tickets' | \
            python3 -c \
            "import sys, json; print(json.load(sys.stdin)['$line'])")
    done

    # "Get Results for a Batch Search" endpoint retrieves alignment search results
    # corresponding to the ticket issued for a batch search request.
    # Returns a JSON object containing data for any alignments found for the query
    # sequence against the target namespace, as well as metadata for the given namespace.
    # It has two query parameters:
    # 1) offset	An optional 0-based index from which to start retrieving results (default: 0)
    # 2) N	The maximum number of results to retrieve (default: retrieves all results)
    curl --silent https://genesearch.kbase.us/ticket/$line > $json_dumps/$line.json
done < $ftickets
