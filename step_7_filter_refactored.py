import argparse

TARGET_IDX = 1  # type: int
args = None


def parse_arguments():
    global args
    parser = argparse.ArgumentParser(description="To be filled later.")
    parser.add_argument("-j", "--jcfiltered", type=str)
    parser.add_argument("-r", "--refactored", type=str)
    args = parser.parse_args()


def get_jc_targets(fasta_file):
    lines = None
    targets = []
    with open(fasta_file, 'r') as ff:
        lines = ff.readlines()
    for line in lines:
        if line.startswith('>'):
            targets.append(line.split()[TARGET_IDX].strip())
    return targets


def main():
    global args
    parse_arguments()
    jc_targets = get_jc_targets(args.jcfiltered)
    refactored_lines = None
    with open(args.refactored, 'r') as rf:
        refactored_lines = rf.readlines()
    filtered_lines = []
    # meta_table = {}
    for lineIdx, line in enumerate(refactored_lines):
        if not line.startswith('>'):
            continue
        split_line = line.split()
        target = split_line[TARGET_IDX].strip()
        # target_info = ' '.join(split_line[TARGET_IDX+1:])
        if target in jc_targets:
            # id_line = "> " + '_'.join([target, target_info + '\n'])
            # filtered_lines.append(id_line)
            filtered_lines.append(refactored_lines[lineIdx])
            filtered_lines.append(refactored_lines[lineIdx + 1])
        else:
            print("Skipped %s.." % target)
    filtered_fasta = args.refactored.split('.fa')[0] + "_trimmed.fa"
    with open(filtered_fasta, 'w') as ff:
        ff.write(''.join(filtered_lines))
    print("# of sequences originally: %d" % (len(refactored_lines)/2))
    print("# of sequences after trimming: %d" % (len(filtered_lines)/2))

if __name__ == "__main__":
    main()
