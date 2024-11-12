#!/bin/bash
set -a # automatically export all variables
source .env_rsp
set +a

curl --header "PRIVATE-TOKEN: $ACCESS_TOKEN" "https://fiztexlab-dev.servebeer.com/api/v4/projects/1/packages/generic/binaries/v$VERSION/rsp.linux-amd64.so" --output rsp.linux-amd64.so