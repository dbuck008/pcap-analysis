#!/bin/bash

# convert the pcap to csv so that we can process it with python pandas
# use the 'param_list.txt' file to change what paramters we want in the csv

# Check if the correct number of arguments is provided
if [ $# -ne 2 ]; then
  echo "Usage: $0 <input_file> <output_file>"
  exit 1
fi

# build the filter
filter=""
while read -r line; do
filter="$filter -e $line"
done < "files/param_list.txt"

# build the csv (from one pcap file for now) todo: build csv from multiple pcal files
tshark -T fields $filter -E header=y -r $1 > $2

