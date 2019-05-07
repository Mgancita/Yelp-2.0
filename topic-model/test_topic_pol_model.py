import os

from gensim import corpora
from gensim import models
from gensim.parsing.preprocessing import STOPWORDS
from gensim.parsing.preprocessing import  strip_multiple_whitespaces
from gensim.parsing.preprocessing import strip_punctuation
from gensim.utils import simple_preprocess
import pandas as pd
from pattern.en import sentiment 

path_to_master = '/Users/asnafatimaali/Documents/GitHub/Yelp-2.0'

#path_to_master = os.getcwd()

lda = models.LdaModel.load(os.path.join(path_to_master, 'topic_model','model_data','lda.model'))

lda.per_word_topics = True

#lda.print_topics()


topic_names = { 0:"Bar/Drinks", 1:"Customer Service", 2:"Timely", 3:"Environment/Stay",4:"Location",
5:"Food", 6:"Variety/Order Selection"}


topic_filter = 0.14 # LDA will process topics greater than 14% 

df = pd.read_csv("/Users/asnafatimaali/Desktop/STEVENS/BIA660/Project/Yelp-2.0-master/data/reviews.csv", encoding = "utf-8")
df_need = df["description"]

def tokenize(review):
    
    """ Remove white spaces, punctuations, stop words """
    
    token = strip_multiple_whitespaces(strip_punctuation(review))
    return [token.split() for token in simple_preprocess(token) if token not in STOPWORDS]


def unnest(given):
    
    """ unnest nested lists """
    
    unnested = [m for n in given for m in n]
    return unnested

def topic_model (tokens):
    
    """ create a dictionary, a document matrix, perform the uploaded lda model, and get the topics above the specified filter"""
    
    word2id = corpora.Dictionary(tokens)
    corpo = word2id.doc2bow(simple_preprocess(sentence))
    mod = lda[corpo]
    filtered_topics = lda.get_document_topics(corpo, minimum_probability = topic_filter)
      
    return toke, word2id, mod, filtered_topics

def backwards (num):
    
    """ For the words from the lda model, match the number representation to the actual word from the dictionary """
    
    for key, value in dicto.token2id.items():    
        if value == num:
            dict_word = key
            return(dict_word)

def duplicates(dict_word):
    
    """ Take the word from the dictionary and match it to the tokenized sentence. Grab the indexes where the word matched """
    
    return [i for i, x in enumerate(toke) if x == dict_word]

class WordProcessing:
    
    def filtered_words(topic_ids):
        
        """ get the words(number representations) from the lda model where their first ranked topic is in the topic_ids list"""
        
        words = [idx[0] for idx in modified_word_ids if idx[1][0] in topic_ids]
            
        return words
    
    def word_topic (words, topics):
        
        """ combine the list of words(number representation) from the lda model to the their respective topics """
        
        words_their_topics = dict(list(zip(words,topics))) # combine the words and their respective topic numbers together 
        wordtop_combo = {} # initializing empty dictionary 
        for key, value in sorted(words_their_topics.items()):
            wordtop_combo.setdefault(value, []).append(key)
        wordtop_combo = [x for x in wordtop_combo.items()] # make the above dictionary into a list (easier to use)
        wordsnum_list = [wordlst[1] for wordlst in wordtop_combo]
        topic_numbers = [topicnum[0] for topicnum in wordtop_combo]
            
        return wordsnum_list, topic_numbers

def sentence_from_index(word_lst):
    
    """ get the actual words from the original tokenized sentence to create a list of words for the respective topic """ 
    
    toke_index = [duplicates(backwards(num)) for num in word_lst]
    toke_index = unnest(toke_index)
    toke_index.sort()
    sentence_per_topic_list = [toke[index] for index in toke_index]
        
    return sentence_per_topic_list

def sentences_for_topics(sentence_per_topic_list):
    
    """ create sub sentences from the words associated to the topic from the tokenized sentence (the output of the sentence_from_index function) """
    
    sentence_per_topic = ""
    for word in sentence_per_topic_list:
        sentence_per_topic = sentence_per_topic + " " + word 
    
    return sentence_per_topic
        

topic_senti = []
#counter = 0 

for x in df_need: # reading reveiews cell by cell
        
    topsent = {key: [] for key in list(range(len(topic_names)))} # initialized dictionary to store the polarity score for each sentence, resets for each review
    toappend = {} # initialized ditionary to store the average polarity for each review, calculated from the aformentioned dictionary 
    sentences = x.split(".")
    
    for sentence in sentences: # reading each sentence per review 
        tokens = tokenize(sentence)
        toke = unnest(tokens)
        
        if tokens == []:
            del tokens
            
        else:
            toke, dicto, model, filtered_topics = topic_model(tokens)
            modified_word_ids = [idx for idx in model[1] if idx[1] != []] # some words are not related to any topic, lda represents it with []
                
            if len(filtered_topics) > 1: # if there are more than one topics associated with a sentence after applying the filter
                topic_ids = [num[0] for num in filtered_topics] # get the multiple topics
                words = WordProcessing.filtered_words(topic_ids) # get the words associated to topics_id
                topics = [idx[1][0] for idx in modified_word_ids if idx[1][0] in topic_ids] 
                wordsnum_list, topic_numbers = WordProcessing.word_topic(words, topics)
                
                for y in range(len(wordsnum_list)):
                    polarity = sentiment(sentences_for_topics(sentence_from_index(wordsnum_list[y])))
                    topsent[topic_numbers[y]].append(polarity[0])

            else: # for cases where there is only one topic, after applying the filter, to the sentence
                topic_ids = [filtered_topics[0][0]] # this is if one topic
                words = WordProcessing.filtered_words(topic_ids) # this is if one topic 
                polarity = sentiment(sentences_for_topics(sentence_from_index(words)))
                topsent[topic_ids[0]].append(polarity[0])
                    
    for key, value in topsent.items():
        
        if value == []: # cases where the topic was not associated to the sentence, so the list will be empty 
            del value 
            
        else:
    
            if len(value) > 0:
                score = round(sum(value)/len(value),2)
                toappend[topic_names[key]] = score
    topic_senti.append(toappend)
    
    #print(counter)
    #counter += 1


#print(topic_senti)

df["topic_senti"] = topic_senti 


df.to_csv(os.path.join(path_to_master, "data", "reviews_topics_polarity.csv"))
