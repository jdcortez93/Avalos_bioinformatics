#!/bin/bash
cd xml_dumps
prefixed_full="targets_PF00920_full_prefixed"
prefixed_seed="targets_PF00920_seed_prefixed"
# mv $prefixed_full/*.xml PF00920_full_targets_uniprot/.
# mv $prefixed_seed/*.xml PF00920_seed_targets_uniprot/.
# rm -rf $prefixed_full/ $prefixed_seed/
cd ..
missed_target_dir="missed_from_db_mapping/targets_PF00920/"
cat $missed_target_dir/$prefixed_full.txt >> pf_targets/PF00920_full_targets_uniprot.txt
cat $missed_target_dir/$prefixed_seed.txt >> pf_targets/PF00920_seed_targets_uniprot.txt