import json

f1 = "15_ilvD_E.coli.json"
f2 = "14_ilvC_E.coli.json"

def prettify(f):
    data = None
    with open(f, 'r') as fp:
        data = json.load(fp)
    f_mod = f.split('.json')[0] + "_pretty.json"
    with open(f_mod, 'w') as fp:
        fp.write(json.dumps(data, indent=4))

# prettify(f1)
# prettify(f2)

f = "xml_dumps/15_ilvD_E.coli_targets/annotated_info.txt"
prettify(f)
