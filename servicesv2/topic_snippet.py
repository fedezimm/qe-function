def getDesambiguationTerms(topic, model, id2word):
  expand = []
  # Initialize a list--
  desambiguation_terms = []
  # For each term in topic: --
  for term in topic[0][1]:
    # Store None value in variable X --
    desambiguation_term = term[0]
    best_word = term[0]
    print("term: "+ desambiguation_term)
    try:
      WikipediaPage(desambiguation_term).content
      print("ejecucion correcta con el termino " + desambiguation_term)
      desambiguation_terms.append(desambiguation_term)
      expand.append(True)

    # If there is a DesambiguationError (except) --
    except PageError:
      print('PageError para el termino '+ desambiguation_term)
    except DisambiguationError as err:
      print("DisambiguationError para el termino " + desambiguation_term)
      value = 0
      best_word = term[0]
      # Iterate throw each DesambiguationOption and extract from each the word in parenthesis--
      for option in err.options:
        print(f'Alternativa: {str(option)}', end=" ")
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
      # Append variable X in the list (else)
      desambiguation_terms.append(desambiguation_term)
      expand.append(False)

  return desambiguation_terms, expand # [True, False, True]
