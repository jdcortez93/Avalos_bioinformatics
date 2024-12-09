import glob
import json
import os

cwd = os.getcwd()


def process_line(line, meta_table):
    if not line.startswith(">"):
        return meta_table
    genes = ""
    organisms = ""

    idx = 1
    split_line = line.split()
    target = split_line[idx]
    idx += 1

    if split_line[idx].startswith("genes:"):
        genes = split_line[idx].split("genes:")[1]
        idx += 1

    if split_line[idx].startswith("organisms:"):
        organisms = ' '.join(split_line[idx:]).split("organisms:")[1]

    meta_table[target] = {"genes": genes, "organisms": organisms}
    return meta_table


def main():
    all_fasta = glob.glob(cwd + "/refactored_fasta_dumps/*_trimmed.fa")
    for fasta in all_fasta:
        all_lines = None
        with open(fasta, 'r') as ff:
            all_lines = ff.readlines()
        meta_table = {}
        for line in all_lines:
            meta_table = process_line(line, meta_table)
        meta_table_file = fasta.split(".fa")[0] + "_meta.json"
        with open(meta_table_file, 'w') as mf:
            mf.write(json.dumps(meta_table, indent=4))


if __name__ == "__main__":
    main()
