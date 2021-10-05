from wikipedia.exceptions import DisambiguationError
from services.model import prepare_data_model, get_model

def getTopicsFromModel(term):
  corpus, id2word, _, n_topics, _ = prepare_data_model('', [term])
  model = get_model(corpus, id2word, n_topics)
  topic = model.show_topics(num_words=50, formatted=False)
  desambiguation_terms = getDesambiguationTerms(topic)

  return topic, desambiguation_terms

def getDesambiguationTerms(topic):
  # Initialize a list
  desambiguation_terms = []
  # For each term in topic:
  for term in topic:
    # Store None value in variable X
    desambiguation_term = term
    
    try:
      # Search term in wikipedia (try)
      pass
    # If there is a DesambiguationError (except)
    except:
      value = 0
      # Iterate throw each DesambiguationOption and extract from each the word in parenthesis
      for ds_term in err.options:
        # Apply function to that word that returns us a value of belongness to the topic
        # Store the  index that is greater than every case
        if actual_value > value: 
          index = actual_index_value
      # Store the best desambiguation term in variable X
      desambiguation_term = err.options[index]
    # Append variable X in the list (else)
    desambiguation_terms.append(desambiguation_term)
  return desambiguation_terms