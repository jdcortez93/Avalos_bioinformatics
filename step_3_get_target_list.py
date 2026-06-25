import argparse
import glob
import os
import sys

# ---------------------------------------------------
# parse command line arguments into a global variable
# ---------------------------------------------------
def parse_arguments():
    global args
    parser = argparse.ArgumentParser(description = "To be filled later.")
    parser.add_argument("-d", "--fastadir", type = str)
    parser.add_argument("-f", "--fastafile", type = str)
    parser.add_argument("-t", "--targetdir", type = str)
    args = parser.parse_args()


# ------------------------------------
# create appropriate target directory 
# ------------------------------------
def manage_targetdir():
    cwd = os.getcwd()
    target_list_dir = os.path.join(cwd, "target_lists")
    if args.targetdir is not None:
        target_list_dir = args.targetdir
    if not os.path.exists(target_list_dir):
        os.makedirs(target_list_dir)
    return target_list_dir


# ---------------------------------------------------
# parse fasta file and return a list of target IDs
# ---------------------------------------------------
def get_target_ids(fasta):
    target_ids = []
    fa_count = 0
    with open(fasta, 'r') as ff:
        lines = ff.readlines()
    for line in lines:
        if line.startswith('>'):
            target = line.split('>')[1].strip().split('/')[0]
            target_ids.append(target)
            fa_count += 1
    return target_ids, fa_count


# ------------------------------------------------------------
# process all fasta files and write corresp. target list files
# ------------------------------------------------------------
def process_fastas(fastas, target_list_dir):
    """grab UniRef90 IDs per fasta; log them in a target-list file per fasta"""
    for fasta in fastas:
        target_ids, fa_count = get_target_ids(fasta)
        
        """write the target ids for this fasta"""
        target_file = os.path.join(target_list_dir, 
            fasta.split("/")[-1].split(".fa")[0] + '_targets.txt')
        with open(target_file, 'w') as tf:
            tf.write('\n'.join(target_ids))
        
        """perform checks"""
        assert len(target_ids) == fa_count, "some targets are missing/extra."


# --------------
# main function
# --------------
def main():
    parse_arguments()
    target_list_dir = manage_targetdir()
    if args.fastadir is not None:
        fastas = glob.glob(args.fastadir + "/*.fa")
    if args.fastafile is not None:
        fastas = [args.fastafile]
    process_fastas(fastas, target_list_dir)


if __name__ == "__main__":
    main()
