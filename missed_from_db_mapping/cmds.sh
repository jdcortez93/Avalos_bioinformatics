#!/bin/bash
dir="targets_PF00920/"
mkdir -p $dir
tail -n +2 mapping_PF00920_seed.txt | cut -d$'\t' -f2 > targets_PF00920_seed.txt
tail -n +2 mapping_PF00920_full.txt | cut -d$'\t' -f2 > targets_PF00920_full.txt
sed 's/^/UniRef90_/' targets_PF00920_seed.txt > $dir/targets_PF00920_seed_prefixed.txt
sed 's/^/UniRef90_/' targets_PF00920_full.txt > $dir/targets_PF00920_full_prefixed.txt
