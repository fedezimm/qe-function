import nltk
from gensim.parsing.preprocessing import remove_stopwords
import wikipedia
from gensim.models import Phrases
from nltk.tokenize import RegexpTokenizer
from gensim.corpora import Dictionary
from gensim.models import LdaModel

def donwload_dependencies():
  pass
  # nltk.download('averaged_perceptron_tagger')
  # #nltk.download('wordnet')
  # nltk.download('stopwords')
  # conll2000 = nltk.download('conll2000')

language = 'english'
en_stop = set(nltk.corpus.stopwords.words(language))

def clean_text(lista):
  output = []
  for word in lista:
    if remove_stopwords(word) != '':
      output.append(remove_stopwords(word))
  return output

def add_n_grams(corpus, min_count=3):
  # Add bigrams and trigrams to docs (only ones that appear 3 times or more).
  n_gram = Phrases(corpus, min_count=min_count)
  for idx in range(len(corpus)):
      for token in n_gram[corpus[idx]]:
          if '_' in token:
              # Token is a bigram, add to document.
              corpus[idx].append(token)
  return corpus

def prepare_data_model(query, extra_terms = []):
  clean_key = extra_terms
  # Paso 3.1
  # retrieve wikipedia pages
  # pesticide residues treatment and ecological waste
  corpus = []
  for k in clean_key:     
      try:
          retrieve_doc = wikipedia.WikipediaPage(k).content #Retrieval information from Wikipedia of the first term
          retrieve_doc = retrieve_doc.replace("=", "") #Clean the document
          retrieve_doc = retrieve_doc.replace("\n\n\n","") #Clean the document
          retrieve_doc = retrieve_doc.split("\n") #Split the retrieve extense doc in a list smaller docs (differents paragraphs)
          paragraphs = []
          for doc in retrieve_doc:
              if len(doc)>250:
                  paragraphs.append(doc)
          corpus.append(paragraphs)
      except:
          pass
  busq_efect = len(corpus)
  together = []
  for doc in corpus:
      together+=doc
  corpus = together
  # Paso 4.1
  # Tokenize the documents, that is split the documents into tokens.
  tokenizer = RegexpTokenizer(r'\w+')
  for idx in range(len(corpus)):
      corpus[idx] = corpus[idx].lower()  # Convert to lowercase.
      corpus[idx] = tokenizer.tokenize(corpus[idx])  # Split into words.
      corpus[idx] = [word for word in corpus[idx] if word not in en_stop] #drop the stop words.
      corpus[idx] = clean_text(corpus[idx])
  # Paso 4.2
  # Remove numbers, but not words that contain numbers.
  corpus = [[token for token in doc if not token.isnumeric()] for doc in corpus]
  # Remove words that are only 3 characteres.
  corpus = [[token for token in doc if len(token) > 2] for doc in corpus]
  # Paso 4.3
  # Compute collocations
  corpus = add_n_grams(corpus)
  # Paso 4.4
  # Create a dictionary representation of the documents.
  id2word = Dictionary(corpus)

  # Paso 4.5
  # Filter out words that occur less than 20 documents, or more than 50% of the documents.
  id2word.filter_extremes(no_below=5, no_above=0.95)
  # Bag-of-words representation of the documents.
  bag_corpus = [id2word.doc2bow(doc) for doc in corpus]
  #Check the number of unique tokens and the number of documents
  #temp = dictionary[0]  # This is only to "load" the dictionary.
  #id2word = dictionary.id2token
  return bag_corpus, id2word, corpus, busq_efect, clean_key

def get_model(bag_corpus, id2word, num_topics, alpha = 'auto', eta='auto'):  
  # Paso 5.1
  # Set training parameters.
  num_topics = num_topics #Number of topics we want to obtain from the corpus 
  chunksize = 100 #Number of documents to be used in each training chunk
  passes = 10 #Number of passes through the corpus during training.
  iterations = 4000 #Iterations that do the LDA model to assign for each word of a document the more probable topic (Training iterations)
  alpha=0.01

  model = LdaModel(
      corpus=bag_corpus,
      id2word=id2word,
      chunksize=chunksize,
      alpha=alpha,
      eta=eta,
      #iterations=iterations,
      num_topics=num_topics,
      passes=passes,
      random_state=3)
  
  return model
