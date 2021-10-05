from services.topic import getTopicsFromModel
import json

def getTopic(term):
  topics, desambiguation_terms = getTopicsFromModel(term)
  response = {
    'key': [term],
    'topics': [{
      'id': topic[0],
      'keys': [{
        'word': topic[1][index][0], #character
        'value': str(topic[1][index][1]), #0.001
        'ds_term': desambiguation_terms[index] #character (novel)
      } for index in range(len(topic[1]))]
    } for topic in topics]
  }
  return json.dumps(response)


  #batman y superman
  #['batman','superman']
  #[(world,092,world), (character,097,[character(novel), character(film)]), new york, guason), (character, pelirroja, azul, rojo)]
  #[0]