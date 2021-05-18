import argparse
import glob
import json
import sys
import xml.etree.ElementTree as ET


def parse_arguments():
    global args
    parser = argparse.ArgumentParser(description="To be filled later.")
    parser.add_argument("-a", "--xmldirall", type=str)
    parser.add_argument("-x", "--xmldir", type=str)
    args = parser.parse_args()


# For each XML file, grab the genes and organisms if present
# Dump all this information in a JSON inside all directories
# within xml_dumps in a file called annotated_info.txt
def process_xml(xml):
    info = {\
        "metadata" : "", \
        "sequence" : "", \
        "taxonomy": ""}
    target_id = xml.split('.xml')[0].split('last_')[1]
    try:
        tree = ET.parse(xml)
    except ET.ParseError as etErr:
        print(etErr)
        return target_id, info
    root = tree.getroot()
    namespace = "{http://uniprot.org/uniprot}"
    entry = root.find(namespace + 'entry')
    
    """get genes"""
    genes = entry.findall(namespace + 'gene')
    gene_txt = "genes:"
    for gene in genes:
        names = gene.findall(namespace + 'name')
        gene_txt += '|'.join([name.text for name in names])
    if len(genes) == 0:
        gene_txt = ''
    
    """get organisms"""
    organisms_text = "organisms:"
    tax_text = ""
    organisms = entry.findall(namespace + 'organism')
    for organism in organisms:
        names = organism.findall(namespace + 'name')
        organisms_text += '|'.join([name.text for name in names])
        
        """get taxonomy"""
        lineages = organism.findall(namespace + 'lineage')
        for lineage in lineages:
            taxons = lineage.findall(namespace + 'taxon')
            tax_list = [tax.text for tax in taxons]
            tax_json = '|'.join(tax_list)
    if len(organisms) == 0:
        organisms_text = ''
    
    """get full sequence"""
    sequence = entry.findtext(namespace + 'sequence')
    
    """fill JSON"""
    info["metadata"] = gene_txt + ' ' + organisms_text
    info["taxonomy"] = tax_json
    info["sequence"] = sequence
    return target_id, info

def process_one_xml_dir(dir):
    xmls = glob.glob(dir + '/*.xml')
    with open(dir + '/annotated_info.json', 'w') as af:
        annotations = {}
        for xml in xmls:
            target, info = process_xml(xml)
            annotations[target] = info
        af.write(json.dumps(annotations, indent=4))
    assert len(xmls) == len(annotations)

    tax_table_lines = []
    with open(dir + '/annotated_info.json', 'r') as af:
        json_data = json.load(af)
        for target in json_data:
            tax = '\t'.join(json_data[target]["taxonomy"].split('|'))
            tax_table_lines.append(target + '\t' + tax)
    with open(dir + '/tax_table.tsv', 'w') as tf:
        tf.write('\n'.join(tax_table_lines))  

def main():
    global args
    parse_arguments()
    if args.xmldirall is not None:
        dirs_in_xml = glob.glob(args.xmldirall + '/*')
        for dir in dirs_in_xml:
            process_one_xml_dir(dir)
    if args.xmldir is not None:
        process_one_xml_dir(args.xmldir)
        


if __name__ == "__main__":
    main()
