from __future__ import print_function
import argparse
import os
import requests
import subprocess
import sys

MAXHITS=10
url = "https://www.uniprot.org/uniprot/"

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
    parser.add_argument("-s", "--seqhits", type = str)
    parser.add_argument("-d", "--domainhits", type = str)
    parser.add_argument("-t", "--targetlist", type = str)
    parser.add_argument("-o", "--outdir", type = str, default = './')
    args = parser.parse_args()

# ---------------------------------------------------------
# parse jackHMMER hits table file and query UniProt via URL
# ---------------------------------------------------------
def parse_hits_table(hits_file):
    with open(hits_file, 'r') as hits_file_ptr:
        data = hits_file_ptr.readlines()
    keep = []
    for index, line in enumerate(data):
        if not line.startswith('#'):
            keep.append(index)
    data = [data[index] for index in keep]
    data = data[:MAXHITS] if len(data) > MAXHITS else data
    targets = []
    for line in data:
        targets.append(line.split()[0])
    return targets


# ---------------------------------------------------------
# log errors in exception handling block
# ---------------------------------------------------------
def exception_handling(err, hit_url):
    eprint("exception: %s" % err)
    error = sys.exc_info()[0]
    eprint("error: %s" % error)
    eprint("\nLogs for debugging:")
    eprint("Hit URL: %s" % hit_url)


# ---------------------------------------------------------
# try generating XMLs with two methods: requests and WGET
# ---------------------------------------------------------
def generate_xmls(targets, prefix):
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    
    success_xmls = []
    for query in targets:
        print(query)
        query = query.split('_')[1]
        hit_url = url + query + ".xml"
        
        """if XML already exists"""
        if hit_url in success_xmls:
            print("%s has already been extracted." % hit_url)
            continue
        
        """method i: requests library"""
        response = None
        xml_file_name = args.outdir + '/' + prefix + "_" + query + ".xml"
        try:
            response = requests.get(hit_url, allow_redirects = True, timeout = 30)
            open(xml_file_name, 'wb').write(response.content)
        except requests.exceptions.Timeout:
            eprint("requests.error: ran too long")
        except Exception as err:
            if response is not None:
                eprint(response.status_code)
            exception_handling(err, hit_url)

        if os.path.exists(xml_file_name):
            success_xmls.append(hit_url)
            continue
        
        """method ii: WGET"""
        try:
            result = subprocess.run(["wget", "-O", xml_file_name, hit_url],
                stdout = subprocess.PIPE, stderr = subprocess.PIPE, timeout = 10)
        except subprocess.TimeoutExpired:
            eprint('subprocess.error: wget ran too long')
        except Exception as err:
            eprint("subprocess.error: %s" % result.stderr)
            exception_handling(err, url)

        if os.path.exists(xml_file_name):
            success_xmls.append(hit_url)
            continue


def parse_target_list():
    ftarget = open(args.targetlist, 'r')
    targets = ftarget.readlines()
    targets = [t.strip() for t in targets]
    ftarget.close()
    return targets

def main():
    parse_arguments()
    if args.targetlist is not None:
        generate_xmls(parse_target_list(), "last")
        sys.exit()
    generate_xmls(parse_hits_table(args.seqhits), "seq")
    generate_xmls(parse_hits_table(args.domainhits), "dom")

if __name__ == "__main__":
    main()
