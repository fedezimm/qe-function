from nltk.tag import UnigramTagger, BigramTagger
from nltk.chunk import ChunkParserI
from nltk.corpus import conll2000
from nltk.chunk.util import tree2conlltags,conlltags2tree
from nltk import pos_tag

data = conll2000.chunked_sents()
train_data = data[:10900]
test_data = data[10900:]
wtc=tree2conlltags(train_data[1])
tree=conlltags2tree(wtc)

def conll_tag_chunks(chunk_sents):
    tagged_sents = [tree2conlltags(tree) for tree in chunk_sents]
    return [[(t, c) for (w, t, c) in sent] for sent in tagged_sents]
def combined_tagger(train_data, taggers, backoff=None):
    for tagger in taggers:
        backoff = tagger(train_data, backoff=backoff)
    return backoff

#Define the chunker class
class NGramTagChunker(ChunkParserI):
    def __init__(self,train_sentences,tagger_classes=[UnigramTagger,BigramTagger]):
        train_sent_tags = conll_tag_chunks(train_sentences)
        self.chunk_tagger = combined_tagger(train_sent_tags,tagger_classes)
    
    def parse(self,tagged_sentence):
        if not tagged_sentence:
            return None
        pos_tags = [tag for word, tag in tagged_sentence]
        chunk_pos_tags = self.chunk_tagger.tag(pos_tags)
        chunk_tags = [chunk_tag for (pos_tag,chunk_tag) in chunk_pos_tags]
        wpc_tags = [(word,pos_tag,chunk_tag) for ((word,pos_tag),chunk_tag) in zip(tagged_sentence,chunk_tags)]
        return conlltags2tree(wpc_tags)

#train chunker model
ntc=NGramTagChunker(train_data)

class Query(object):
    def __init__(
        self,
        query
    ):
        self.value = query
        self.terms = self.get_terms(query)
    
    def get_terms(self, query):
        nltk_pos_tagged = pos_tag(query.split())
        chunk_tree = ntc.parse(nltk_pos_tagged)
        
        print('Arbol armado de la consulta: ',chunk_tree)
        print('')
        key = []
        
        for ph in chunk_tree:
            sub_k = ""
            for elem in ph:
                sub_k += elem[0] + " "
            sub_k = sub_k.replace(',', '')
            sub_k = sub_k.replace('.', '')
            sub_k = sub_k.replace('/', '')
            sub_k = sub_k[:-1]
            if len(sub_k) > 4:
                key.append(sub_k)
        
        return key