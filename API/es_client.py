from elasticsearch import Elasticsearch

class ESClient:
  def __init__(self):
    self.es = Elasticsearch("http://localhost:9200")

  def extract_songs(self, resp):
    songs = []
    hits = resp["hits"]["hits"]
    for i in range(len(hits)):
      songs.append(hits[i]["_source"])
    return songs
  
  def get_all_songs(self):
    resp = self.es.search(index="sinhala-songs-corpus", body={"query": {"match_all": {}}})
    return self.extract_songs(resp)

  def get_logical_combinations(self, req_body):
    resp = None
    if req_body["operation"] == "and":
      resp = self.es.search(index="sinhala-songs-corpus",body={
        "query": {
          "bool": {
            "must": [
              { "match" : { req_body["key1"]+".case_insensitive_and_inflections" : req_body["value1"] } },
              { "match" : { req_body["key2"]+".case_insensitive_and_inflections" : req_body["value2"] } }
            ]
          }
        }
      })
    elif req_body["operation"] == "or":
      resp = self.es.search(index="sinhala-songs-corpus",body={
        "query": {
          "bool": {
            "should": [
              { "match" : { req_body["key1"]+".case_insensitive_and_inflections" : req_body["value1"] } },
              { "match" : { req_body["key2"]+".case_insensitive_and_inflections" : req_body["value2"] } }
            ]
          }
        }
      })
    elif req_body["operation"] == "not":
      resp = self.es.search(index="sinhala-songs-corpus",body={
        "query": {
          "bool": {
            "must" : {
              "match" : { req_body["key1"]+".case_insensitive_and_inflections" : req_body["value1"] }
            },
            "must_not" : {
              "match" : { req_body["key2"]+".case_insensitive_and_inflections" : req_body["value2"] }
            }
          }
        }
      })
    return self.extract_songs(resp)
    
    
    
 
