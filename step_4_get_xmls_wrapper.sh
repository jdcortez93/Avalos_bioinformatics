#!/bin/bash
target_dir=$1
mkdir -p xml_dumps

# For each fasta-target list file in the target list dir
# call the get_xmls py script that generates xmls for
# each target in the target list file supplied to it.
for ftarget in $target_dir/*; do
  name=$(basename -- "$ftarget")
  name="${name%.*}"
  mkdir -p xml_dumps/$name
  python3 step_4_get_xmls_9.0.0.py -t $ftarget -o xml_dumps/$name/
done
