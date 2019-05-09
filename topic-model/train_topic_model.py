import os

import gensim
from gensim import corpora
from gensim.parsing.preprocessing import STOPWORDS
from gensim.parsing.preprocessing import  strip_multiple_whitespaces
from gensim.parsing.preprocessing import strip_punctuation
from gensim.utils import simple_preprocess
import json


# path to data set intended to use to train model
path_to_dump = '/Users/asnafatimaali/Desktop/STEVENS/BIA660/Project/yelp_dataset'
#path_to dump = os.getcwd()

path_model_storage = '/Users/asnafatimaali/Documents/GitHub/Yelp-2.0/topic-model/model_data'

num_of_topics = 7

def read_file(reviews):
    """ read in one review at a time """

    for review in reviews:
        yield json.loads(review)["text"]

def tokenize(review):
    """ Remove whitespace, punctuations, and stop words from the reviews read in """

    token = strip_multiple_whitespaces(strip_punctuation(review))
    return [token.split() for token in simple_preprocess(token) if token not in STOPWORDS]

tok = [[]]
dictionary = corpora.Dictionary(tok) # initialize dictionary 
final_corpus = [] # initialize corpus

model_type = input("CHOOSE ONE \nA: Create a completely new model \nB: Retrain LDA with different number of topics \n[A/B]:  ")


if model_type == "A": 
    with open (os.path.join(path_to_dump, 'review.json'), 'r', encoding="utf-8") as f:
        for review in read_file(f):
            dicto = corpora.Dictionary(tokenize(review))
            dictionary.merge_with(dicto)
                
    dictionary.save_as_text(os.path.join(path_model_storage, "dictionary.txt"))
    print("Dict Done")
    
    with open (os.path.join(path_to_dump, 'review.json'), 'r', encoding="utf-8") as f:
        for review in read_file(f):
            final_corpus.append(dictionary.doc2bow(simple_preprocess(review)))

    
    corpora.MmCorpus.serialize(os.path.join(path_model_storage, 'corpus.mm'), final_corpus)
    print("Corpus Done") 

    lda = gensim.models.ldamodel.LdaModel(corpus = final_corpus, id2word = dictionary, num_topics= num_of_topics, update_every=1, passes=1)
    
    lda.save(os.path.join(path_model_storage,"lda.model"))

    print("Model DONE!!!!")
    
else:
    dictionary = gensim.corpora.Dictionary.load_from_text(path_model_storage, "dictionary.txt")
    corpus_download = input("Do you have corpus.mm in your directory? \n[Y/N]")
    
    if corpus_download == "Y":
        final_corpus = gensim.corpora.MmCorpus(os.path.join(path_model_storage, 'corpus.mm'))  
        
    else: 
        print ("Download the file from: \n https://drive.google.com/open?id=1kAQS4Nn38IwUmXBxTMwOUd-q8yiReqcJ \n Place it in the directory")
        download = input("Is the corpus in the your directory? \n[Y/N]")
        if download == "Y":
            final_corpus = gensim.corpora.MmCorpus(os.path.join(path_model_storage, 'corpus.mm'))

            lda = gensim.models.ldamodel.LdaModel(corpus = final_corpus, id2word = dictionary, num_topics= num_of_topics, update_every=1, passes=1)
            lda.save(os.path.join(path_model_storage,"lda.model"))

            print("Model DONE!!!!")
        else: 
            print("No model was created")
            

#lda.print_topics()

### NOTES:
# 6,685,900 reviews in dump
# run time of dictionary and corpus is a little over 2 hours 
#lda for about 60 - 65 minutes

