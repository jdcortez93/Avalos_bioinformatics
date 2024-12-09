import glob
import json
import os

# Set up variables for locations corresponding to
# JSON and FASTA dumps
json_files = glob.glob("json_dumps/*.json")
cwd = os.getcwd()
fasta_dir = os.path.join(cwd, "fasta_dumps")
if not os.path.exists(fasta_dir):
    os.makedirs(fasta_dir)

# Iterate over JSON files obtained from the Genesearch tool
for json_file in json_files:
    json_content = None
    with open(json_file, 'r') as jfp:
        json_content = json.load(jfp)
    alignments = json_content["alignments"]
    # Newline separated `targetid` and `targetalignseq` constitute
    # one element in the fasta list. Of course add '>' to make the
    # string `.fa` appropriate.
    fasta = []
    for target_hit in alignments:
        target_id = target_hit["targetid"]
        # target_seq = target_hit["targetalignseq"]
        # fasta.append("> " + target_id + "\n" + target_seq)
        fasta.append("> " + target_id)
    # Store this number for testing purposes; used later in this script
    target_count = len(fasta)

    # Write the `.fa` file. Using '\n'.join ensures that there are no
    # newline characters after the last sequence or before the first.
    fasta_file = os.path.join(fasta_dir, json_file.split('.json')[0].split('/')[-1] + '.fa')
    with open(fasta_file, 'w') as ffp:
        ffp.write('\n'.join(fasta))

    # TESTS--
    # For testing read the written `.fa` file and it must have twice as
    # many lines as the number of lines containing '>' (TEST-1).
    # This file must also have as many lines containing '>' as the target_count
    # stored above (TEST-2).
    with open(fasta_file, 'r') as ffp:
        lines = ffp.readlines()
        # seq_count = len(lines)/2
        seq_count = len(lines)
        seq_start_count = 0
        for line in lines:
            if line.startswith('>'):
                seq_start_count += 1
        assert seq_count == seq_start_count, "Error Pos. 1"
        assert seq_count == target_count, "Error Pos. 2"
