import json
import sys
import glob
import os

cwd = os.getcwd()
refactored_fasta_dumps = os.path.join(cwd, "refactored_fasta_dumps")
if not os.path.exists(refactored_fasta_dumps):
    os.makedirs(refactored_fasta_dumps)

# Read each original fasta one by one
# grab corresponding annotated info for each target
# write the new fastas
input_fastas = glob.glob(cwd + "/fasta_dumps/*.fa")
for fasta in input_fastas:
    print("Processing %s fasta." % (fasta))
    print("-------------------------------")
    annotated_file = cwd + "/xml_dumps/" + \
                     fasta.split('/')[-1].split('.fa')[0] + \
                     "_targets/annotated_info.json"
    annotated_json = None
    with open(annotated_file, 'r') as af:
        annotated_json = json.load(af)

    old_lines = None
    with open(fasta, 'r') as fp:
        old_lines = fp.readlines()
    new_lines = []
    count_404 = 0
    count_dup = 0
    target_set = []
    for line in old_lines:
        if line.startswith(">"):
            target = line.split("UniRef90_")[1].strip()
            if target in target_set:
                count_dup += 1
                print("dup. Target %s has already been processed and added." % target)
                continue
            if target not in annotated_json:
                count_404 += 1
                print("404. Sequence for %s was not found. Skipping." % (target))
                continue
            annotated_info = annotated_json[target]
            metadata = annotated_info["metadata"]
            sequence = annotated_info["sequence"]
            if sequence == "":
                count_404 += 1
                print("404. Sequence for %s was not found. Skipping." % (target))
                continue
            new_lines.append(line.strip() + ' ' + metadata)
            new_lines.append(sequence)
            target_set.append(target)
    #print(fasta.split('/')[-1].split('.fa')[0] + "_refactored.fa")
    with open(refactored_fasta_dumps + '/' + \
              fasta.split('/')[-1].split('.fa')[0] + "_refactored.fa", 'w') as rf:
        rf.write('\n'.join(new_lines))
    print("Total Duplicates removed: %d" % count_dup)
    print("Total Skipped: %d" % count_404)
    print("-------------------------------")
