from django.db import models
import os
import xmltodict
import pickle
import re
from functools import reduce
import numpy as np
from nltk.corpus import stopwords 
from django.conf import settings
from nltk.stem import PorterStemmer

ps = PorterStemmer() 

query_conf_file=open(os.path.join(settings.BASE_DIR, 'conf/queryconf.xml'))
root_path = os.path.dirname(settings.BASE_DIR)
data_path = root_path+"/index_config/data/"
documents_file="docs.dat"
index_file="{}.idx"



#set stopwords
en_stopwords=set(stopwords.words('english'))

#max_term_frequency
max_term_frequency_ignore=1000


class DataRepo:
    
    documents=[]
    docs_in = open(data_path+documents_file,"rb")
    documents = pickle.load(docs_in)
    
    def __init__(self,queryFields):
        self.inverted_idx={}
        
        for field in queryFields:
            docs_in = open(data_path+index_file.format(field),"rb")
            index = pickle.load(docs_in)
            self.inverted_idx[field]=index


class SearchConfig:
    
    def __init__(self):
        self.queryFields=[]
        self.displayFields=[]
        
        conf = xmltodict.parse(query_conf_file.read())
        for field in conf['queryConf']['searchProfile']['query']['field']:
            self.queryFields.append(field['@name'])
            
        for field in conf['queryConf']['searchProfile']['display']['field']:
            self.displayFields.append(field['@name'])

searchConf=SearchConfig()

dataRepo=DataRepo(searchConf.queryFields)            

class SearchService:
    
    def __init__(self):
        self.totalCount = 0
        self.filteredCount=0
        self.pageSize = 10
        self.pageNum = 1
        self.facetView = []
        self.fq=[]
        self.documentList = []  
        self.filterdDocList =[]
        self.query=None
    
    def populate_facetView(self,idx_list):
        documentList = [dataRepo.documents[idx] for idx in idx_list]
        facetView = []
        topicKey_count={}
        filteredDocs=[]
        for doc in documentList:
            if 'topic' in doc:
                topics=doc['topic']
                for topic in topics:
                    #build filtered doc list
                    if topic['name'] in self.fq:
                        filteredDocs.append(doc)
                    if topic['name'] in topicKey_count:
                        topicKey_count[topic['name']]=topicKey_count[topic['name']]+1;
                    else:
                        topicKey_count[topic['name']]=1
        

        for topic_name,count in topicKey_count.items():
            facet={}
            facet['name']=topic_name
            facet['count']=count
            if facet['name'] in self.fq:
                facet['checked']='checked'
            else:
                facet['checked']=''
            facetView.append(facet)
        
        self.facetView=facetView
        #set filtered results
        if len(filteredDocs) > 0:
            self.filterdDocList=filteredDocs
            self.filteredCount=len(filteredDocs)
                        
    
    def response(self):
        response={}
        if self.filteredCount > 0:
            self.totalCount=self.filteredCount    
        response['totalCount'] = self.totalCount
        response['pageNum'] = self.pageNum
        response['pageSize'] = self.pageSize
        response['fq'] = self.fq
        response['topicFilter'] = self.facetView
        response['docs'] = self.documentList
        return response
        
        
    def build_display_document(self,doc):
        document={}
        for field in searchConf.displayFields:
            if field in doc:
                document[field]=doc[field]
            
        return document


    def filter_stopwords(self,list):
        return [word for word in list if word not in en_stopwords]
    
    def stem_word_list(self,list):
        return [ps.stem(word) for word in list]
    
    def preprocess_string(self,string):
        res_string=re.sub('[^a-zA-Z0-9\s+]+','',string)
        return res_string
    
    def tokenize(self,query):
        word_list=query.split()
        word_list=[word.lower() for word in word_list]
        return word_list
    
    
    def query_inverted_index(self,word_list):
        #idx_list=[inverted_idx[word] for word in word_list if word in inverted_idx]
        idx_aggregate_list=[]
        #dict to intersect all matching words accross query fields
        word_idx_list={}
        for word in word_list:
            for field in searchConf.queryFields:
                #print(field)
                inverted_idx=dataRepo.inverted_idx[field]
                if word in inverted_idx:
                    idx_list=inverted_idx[word]
                    #ignore documet with length > max_term_frequency_ignore 
                    #print(field,word,len(idx_list))
                    #idx_aggregate_list.append(idx_list)
                    if word in word_idx_list:
                        #union word match list
                        word_idx_list[word].append(idx_list)
                    else:
                        word_idx_list[word]=[]
                        word_idx_list[word].append(idx_list)
                        
        
        #merge within words to group among the multiple matching field in index
        for word in word_idx_list:
            #union idx within words from different fields
            #add additional checks here if max_term_frequency to be checked for performance imporvemnt in intersection
            idx_aggregate_list.append(reduce(np.union1d,word_idx_list[word]))
        
        #intersect documents to match all terms
        if len(idx_aggregate_list) > 0:
            reduced_idx_list=reduce(np.intersect1d,(idx_aggregate_list))
            #populate the facetView
            self.populate_facetView(reduced_idx_list)
            #paginate documents based on pageSize and pageNum
            begin_index=(self.pageNum-1)*(self.pageSize)
            end_index=begin_index + self.pageSize
            idx_length=len(reduced_idx_list)
            ####pagination#####
            print(begin_index,end_index)
            if end_index < idx_length:
                if self.filteredCount > 0:
                    self.documentList = [doc for doc in self.filterdDocList[begin_index:end_index]]
                else:
                    self.documentList = [dataRepo.documents[idx] for idx in reduced_idx_list[begin_index:end_index]]
            else:
                if self.filteredCount > 0:
                    self.documentList = [doc for doc in self.filterdDocList[begin_index:]]
                else:
                    self.documentList = [dataRepo.documents[idx] for idx in reduced_idx_list[begin_index:]]
                
            self.totalCount = len(reduced_idx_list)
            
            
        return self.response()

    
    def query_idx(self,q):
        q=self.preprocess_string(q)
        word_list=self.tokenize(q)
        word_list=self.filter_stopwords(word_list)
        word_list=self.stem_word_list(word_list)
        return self.query_inverted_index(word_list)
    
    def search_query_fields(self,params):
        print(params)
        query='q'
        if query in params:
            self.query=params[query]
            print(self.query)
        else:
            return self.response()
        
        pageSize='pageSize'
        if pageSize in params:
            if str(params[pageSize]).isdigit():
                self.pageSize = int(params[pageSize])
        
        pageNum ='pageNum'
        if pageNum in params:
            if str(params[pageNum]).isdigit():
                self.pageNum = int(params[pageNum])
        
        filterQuery='fq'
        if filterQuery in params:
            filterParam=params[filterQuery].split(':')
            self.fq.append(filterParam[1])
            
        return self.query_idx(self.query)
            
        
            
    @staticmethod
    def query(params):
        service=SearchService()
        return service.search_query_fields(params)
        
    