import argparse
import glob
import os
import sys

XML_DIR = os.getcwd() + "/xml_dumps"

# ---------------------------------------------------
# parse command line arguments into a global variable
# ---------------------------------------------------
def parse_arguments():
    global args
    parser = argparse.ArgumentParser(description = "To be filled later.")
    parser.add_argument("-t", "--targetdir", type = str)
    args = parser.parse_args()


def check_file(xml):
    if os.path.exists(xml):
        with open(xml) as xf:
            if "This site is not available at the moment." in xf.read():
                return False
        return True
    return False

def check_xmls(target_file):
    with open(target_file, 'r') as tf:
        targets = tf.readlines()
    xml_dir = XML_DIR + "/" + target_file.split('/')[-1].split('.txt')[0]
    there, not_there = 0, []
    for target in targets:
        xml_file = xml_dir + "/last_" + target.split('_')[1].strip() + ".xml"
        #print(xml_file)
        if check_file(xml_file):
            there += 1
        else:
            not_there.append(target.strip())
    print("XMLs present: %d" % there)
    print("XMLs absent: %d" % len(not_there))
    print("XMLs that should be there: %d" % (len(targets)))
    assert there + len(not_there) == len(targets)
    if len(not_there) == 0:
        return
    
    absent_file = xml_dir + "/absent_targets.txt"
    with open(absent_file, 'w+') as af:
        af.write('\n'.join(not_there))
    print("Absent targets are here:\n%s" % absent_file)
    


def main():
    parse_arguments()
    target_files = glob.glob(args.targetdir + "*.txt")
    for target_file in target_files:
        check_xmls(target_file)


if __name__ == "__main__":
    main()