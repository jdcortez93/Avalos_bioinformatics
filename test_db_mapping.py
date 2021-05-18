import urllib.parse
import urllib.request

url = 'https://www.uniprot.org/uploadlists/'

params = {
'from': 'ACC+ID',
'to': 'ACC',
'format': 'tab',
'query': 'G8AQG4_AZOBR W0PDB3_9BURK C7Z2V6_NECH7 W0PEH0_9BURK W0PA44_9BURK'
# 'query': 'G8AQG4_AZOBR'
}

data = urllib.parse.urlencode(params)
data = data.encode('utf-8')
req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as f:
   response = f.read()
print(response.decode('utf-8'))
