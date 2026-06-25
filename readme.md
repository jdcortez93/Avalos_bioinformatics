| File Name | Description/ Source |
|-----------|---------------------|
| `collect_jsons.sh`                  | A copy of the [this](https://code.jgi.doe.gov/ramanik/last/blob/master/scripts/collect_jsons.sh) script from the [LAST Gitlab repository](https://code.jgi.doe.gov/ramanik/last).
| `last_uniprot_for_ilvc_and_ilvd.sh` | A shell script that runs Jeffrey Johnson's [Genesearch](https://portal.nersc.gov/cfs/kbase/johnson/genesearch/) Web Service/Tool. **Note:** `maxHits=10` query parameter was removed as was present in [this](https://code.jgi.doe.gov/ramanik/last/blob/master/scripts/run_last.sh) script from the [LAST Gitlab repository](https://code.jgi.doe.gov/ramanik/last). 
| `tickets.log`                       | A log of ticket IDs obtained from Genesearch representing queued jobs from the tool.
| `fastas/`                           |  The location of "ilvc" and "ilvd" fasta files obtained from Hugh Salamon from Slack.
| `json_to_fasta.py`                  | Converts JSONs obtained from Genesearch to `.fa` files of target sequences. |
| `json_dumps`                        | Location where Genesearch dumps the JSONs obtained from Genesearch. |
| `fasta_dumps`                       | Location where `json_to_fasta.py` dumps the converted `.fa` files. |
