import argparse

TARGET_IDX = 1  # type: int
args = None


def parse_arguments():
    global args
    parser = argparse.ArgumentParser(description="To be filled later.")
    parser.add_argument("-r", "--ref", type=str, 
        help="Reference FA to filter against")
    parser.add_argument("-t", "--fulltax", type=str, 
        help="Full taxonomy table that needs filtering")
    args = parser.parse_args()


def get_ref_targets(fasta_file):
    lines = None
    targets = []
    with open(fasta_file, 'r') as ff:
        lines = ff.readlines()
    for line in lines:
        if line.startswith('>'):
            targets.append(line.split()[TARGET_IDX].strip().split('_')[1])
    return targets


def main():
    global args
    parse_arguments()
    ref_targets = get_ref_targets(args.ref)

    """get tax lines"""
    tax_lines = None
    with open(args.fulltax, 'r') as tf:
        fulltax_lines = tf.readlines()
    filtered_lines = []

    """get tax info for targets in ref"""
    for lineIdx, line in enumerate(fulltax_lines):
        split_line = line.split('\t')
        target = split_line[0].strip()
        if target in ref_targets:
            filtered_lines.append(fulltax_lines[lineIdx])
        else:
            print("Filtered out %s.." % target)
    
    """write out the filtered tax table"""
    filtered_tax = args.ref.split('.fa')[0] + "_tax.tsv"
    with open(filtered_tax, 'w') as ft:
        ft.write(''.join(filtered_lines))
    print("# of tax targets originally: %d" % len(fulltax_lines))
    print("# of tax targets after trimming: %d" % len(filtered_lines))

if __name__ == "__main__":
    main()
