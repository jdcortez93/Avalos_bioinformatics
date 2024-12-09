import argparse
import glob
import os
import requests
import time
import sys


# ------------------------------
# print error messages to stderr
# ------------------------------
def eprint(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)


# ---------------------------------------------------
# parse command line arguments into a global variable
# ---------------------------------------------------
def parse_arguments():
    global args
    parser = argparse.ArgumentParser(description = "To be filled later.")
    parser.add_argument("-s", "--srcdir", type = str)
    parser.add_argument("-t", "--targetdir", type = str)
    args = parser.parse_args()


# ---------------------------
# get uniprot IDs per ACC ID
# ---------------------------
def get_uniprot_ids(query):
    url = 'https://www.uniprot.org/uploadlists/'
    params = {
        'from': 'ACC+ID',
        'to': 'ACC',
        'format': 'tab',
        'query': query
    }
    response, data = None, ''
    try:
        response = requests.get(url, allow_redirects = True, 
            timeout = 30, params = params)
        data = response.content.decode('utf-8')
    except Exception as err:
        eprint("\nexception: %s" % err)
        error = sys.exc_info()[0]
        eprint("error: %s" % error)
    return data


# -----------------------------------------------
# process each input file; check missed uniprots
# -----------------------------------------------
def process_each_src(src, targetdir):
    with open(src, 'r') as sf:
        lines = sf.readlines()
    lines = [line.strip() for line in lines]
    batch_size = 100
    iterations = len(lines)//batch_size 
    if len(lines) % batch_size != 0:
        iterations += 1
    missed, success_trg, success_qry = [], [], []
    MAX_TRIES = 3
    for idx in range(iterations):
        batch = lines[idx*batch_size:batch_size*(idx+1)]
        query = ' '.join(batch)
        print("Processing batch: %d of size: %d" %(idx, len(batch)))
        for tries in range(MAX_TRIES):
            print("Try #%d.." % (tries + 1))
            uniprot_resp = get_uniprot_ids(query)
            uniprot_resp = uniprot_resp.split('\n')
            uniprot_resp = list(filter(None, uniprot_resp))
            uniprot_resp = uniprot_resp[1:]
            if uniprot_resp != []:
                break
        
        for row in uniprot_resp:
            success_trg.append(row.split('\t')[1].strip())
            success_qry.append(row.split('\t')[0].strip())
        missed += list(set(batch) - set(success_qry))
    
    targetfile = src.split('.txt')[0].split('/')[-1] + "_uniprot.txt"
    success_trg = ["UniRef90_" + trg for trg in success_trg]
    with open(targetdir + '/' + targetfile, 'w') as tf:
        tf.write('\n'.join(success_trg))
    
    #check if missed
    if len(lines) != len(success_trg):
        print("Missed: %d/%d" % (len(missed), len(lines)))
        print(missed)


def main():
    parse_arguments()
    src_files = glob.glob(args.srcdir + "/*.txt")
    cwd = os.getcwd()
    targetdir = os.path.join(cwd, args.targetdir)
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    for src in src_files:
        print("Processing %s now.." % src)
        process_each_src(src, targetdir)

if __name__ == "__main__":
    main()