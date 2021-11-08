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
  desambiguation_terms = getDesambiguationTerms(topic,model,id2word)
  print('----------------------------------------------------------paso disambiguation_terms terminado----------------------------------------------------------')
  return topic, desambiguation_terms

def getDesambiguationTerms(topic, model, id2word):
  # Initialize a list--
  desambiguation_terms = []
  # For each term in topic: --
  for term in topic[0][1]:
    # Store None value in variable X --
    #print(term)
    desambiguation_term = term[0]
    best_word = term[0]
    print("term: "+ desambiguation_term)
    try:
      WikipediaPage(desambiguation_term).content
      print("ejecucion correcta con el termino " + desambiguation_term)
    # If there is a DesambiguationError (except) --
    except PageError:
      print('PageError para el termino '+ desambiguation_term)
    except DisambiguationError as err:
      print("DisambiguationError para el termino " + desambiguation_term)
      value = 0
      best_word = term[0]
      # Iterate throw each DesambiguationOption and extract from each the word in parenthesis--
      print('Por entrar')
      for option in err.options:
        print(f'Alternativa: {str(option)}')
        index_start = option.find('(') + 1
        index_final = option.find(')')
        if index_start != -1 and index_final != -1:
          clean_term = option[index_start:index_final]
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
              
      len(err.options)
      # Store the best desambiguation term in variable X
      desambiguation_term = best_word
    # Append variable X in the list (else)
    desambiguation_terms.append(desambiguation_term)
    print(f'Desambiguacion: {str(term[0])} -> {str(best_word)}')
    if term[0] == best_word:
      raise Exception(f'Error en desambiguacion {str(term[0])} -> {str(best_word)}')
  return desambiguation_terms