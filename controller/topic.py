from services.topic import getTopicsFromModel
import json

def getTopic(term):
  topics = getTopicsFromModel(term)
  response = {
    'key': [term],
    'topics': [{
      'id': topic[0],
      'keys': [{
        key[0]: str(key[1])
      } for key in topic[1]]
    } for topic in topics]
  }

  return json.dumps(response)