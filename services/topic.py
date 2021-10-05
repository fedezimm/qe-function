from services.model import prepare_data_model, get_model

def getTopicsFromModel(term):
  corpus, id2word, _, n_topics, _ = prepare_data_model('', [term])
  model = get_model(corpus, id2word, n_topics)
  return model.show_topics(num_words=50, formatted=False)
