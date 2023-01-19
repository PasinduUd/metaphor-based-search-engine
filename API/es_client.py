from elasticsearch import Elasticsearch
from search import search_user_query

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

  def advanced_search(self, req_body):
    filled_keys = {k: v for k, v in req_body.items() if v}
    must_list = []
    for k in filled_keys.keys():
      must_list.append({ "match" : { k+".case_insensitive_and_inflections" : req_body[k] } })
    resp = self.es.search(index="sinhala-songs-corpus",body={"query": {"bool": {"must": must_list}}})
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

  def regular_search(self, req_body):
    resp = search_user_query(req_body["query"], self.es)
    return self.extract_songs(resp)