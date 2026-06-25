#!/bin/bash
cwd=`pwd`
label="pf00920"
# python3 step_3_get_target_list.py -d $cwd/pf_fastas/ -t pf_fastas
# python3 step_3a_get_uniprot_ids.py -s $cwd/pf_fastas -t pf_targets
# bash step_4_get_xmls_wrapper.sh $cwd/pf_targets

## no need to do the next line if step_3b was run before step_4
## bash step_4_get_xmls_wrapper.sh $cwd/missed_from_db_mapping/targets_PF00920

# python3 step_4b_get_failed_xmls_doublecheck.py -t $cwd/pf_targets/ > "$label"_xml_stats.txt

## if there are errored/failed XMLs:: try again
# failed_target_dir="xml_dumps/PF00920_full_targets_uniprot"
# failed_targets=$cwd/$failed_target_dir/"absent_targets.txt"
# python3 step_4_get_xmls_9.0.0.py -t $failed_targets -o $failed_target_dir

## check again
# python3 step_4b_get_failed_xmls_doublecheck.py -t $cwd/pf_targets/

### GOOD TO GO!! ###
# python3 step_5_mine_xml.py -x $cwd/xml_dumps/PF00920_full_targets_uniprot
# python3 step_5_mine_xml.py -x $cwd/xml_dumps/PF00920_seed_targets_uniprot

### NOTE: Even after these checks, in SEED, C4LJI1 had an empty XML file

