#!/bin/bash

echo "downloading data"
./get_json.sh || (echo "getting data failed" && echo "end" && exit 1)

echo "successful end"
