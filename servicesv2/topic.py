from wikipedia import WikipediaPage
from wikipedia.exceptions import DisambiguationError,PageError
from servicesv2.model import prepare_data_model, get_model

def getTopicsFromModel(term):
  print(term)
  corpus, id2word, _, n_topics, _ = prepare_data_model('', [term])
  print('----------------------------------------------------------paso prepare_data_model terminado----------------------------------------------------------')
  model = get_model(corpus, id2word, n_topics)
  print('----------------------------------------------------------paso model terminado----------------------------------------------------------')
  topic = model.show_topics(num_words=50, formatted=False)
  print('----------------------------------------------------------paso topic terminado----------------------------------------------------------')
  desambiguation_terms, expand = getDesambiguationTerms(topic,model,id2word)
  print('----------------------------------------------------------paso disambiguation_terms terminado----------------------------------------------------------')
  return topic, desambiguation_terms, expand

def getDesambiguationTerms(topic, model, id2word):
  # Initialize a list--
  desambiguation_terms = []
  expand = []
  # For each term in topic: --
  for term in topic[0][1]:
    # Store None value in variable X --
    desambiguation_term = term[0]
    best_word = term[0]
    print("term: "+ desambiguation_term)
    try:
      WikipediaPage(desambiguation_term).content
      print("ejecucion correcta con el termino " + desambiguation_term)
      expand.append(True)
    # If there is a DesambiguationError (except) --
    except PageError:
      print('PageError para el termino '+ desambiguation_term)
      expand.append(False)
    except DisambiguationError as err:
      print("DisambiguationError para el termino " + desambiguation_term)
      value = 0
      best_word = term[0]
      # Iterate throw each DesambiguationOption and extract from each the word in parenthesis--
      for option in err.options:
        #print(f'Alternativa: {str(option)}', end=" ")
        clean_term = get_clean_term(option)
        word_id = id2word.token2id.get(clean_term)
        if word_id is not None:
          # Apply function to that word that returns us a value of belongness to the topic --
          actual_value = model.get_term_topics(word_id,0)[0][1]
        else:
          actual_value = 0
        # Store the  index that is greater than every case
        if actual_value > value: 
          best_word = option
          value = actual_value
          print("<--", end=" ")
        print(" ")
      print(f'Desambiguacion: {str(term[0])} -> {str(best_word)}')  
      # Store the best desambiguation term in variable X
      desambiguation_term = best_word
      if desambiguation_term.lower() == term[0].lower():
        expand.append(False)
      else:
        expand.append(True)
    # Append variable X in the list (else)
    desambiguation_terms.append(desambiguation_term)
  return desambiguation_terms, expand

def get_clean_term(term):
  clean_term = term
  index_start = term.find('(') + 1
  index_end = term.find(')')
  if (index_start != -1 and index_end != -1):
    clean_term = term[index_start:index_end]
  clean_term = clean_term.replace(' ', '_').lower()
  return clean_term
