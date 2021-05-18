import json

JSON_FILE = "/global/cscratch1/sd/ramanik/last/scripts/backend_jsons/ureases_v10.pfamcomment.json"

def main():
    gene_list = []
    jf = open(JSON_FILE, 'r')
    data = json.load(jf)
    jf.close()
    geneclusters = data['geneclusters']
    for cluster in geneclusters:
        genes = cluster['genes']
        for gene in genes:
            gene['cluster_id'] = cluster['cluster_id']
            gene_list.append(gene)



if __name__ == "__main__":
    main()