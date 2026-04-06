#!/bin/bash

set -ex

response=$(trino --server localhost:8080 --execute "SHOW CATALOGS LIKE 'tpch'")
if echo "$response" | grep -q tpch; then
  echo "Trino has started"
else
  echo "Trino is not yet finished"
  exit 1
fi

exit 0
