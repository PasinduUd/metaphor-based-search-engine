from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

# resp = es.search(index="sinhala-songs-corpus", query={"match_all": {}})
# print(resp['result'])

print(es.ping())