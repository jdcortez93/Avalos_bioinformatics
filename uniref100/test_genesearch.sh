#!/bin/bash
#fs=$1
#curl --silent -F file=@$fs https://genesearch2.kbase.us/namespace/uniref100/batch

curl -X POST -H "Content-Type: application/json" -d @sample.json https://genesearch2.kbase.us/api/v1/namespaces/uniref100/jobs


# [macos] uniref100 $ bash test_genesearch.sh
# {"id":"123c175e-fed1-46ba-b645-fdb13eda995b","namespace":"uniref100","status":"queued"}
# [macos] uniref100 $ curl https://genesearch2.kbase.us/api/v1/jobs/123c175e-fed1-46ba-b645-fdb13eda995b/status
# {"id":"123c175e-fed1-46ba-b645-fdb13eda995b","namespace":"uniref100","status":"processing"}
