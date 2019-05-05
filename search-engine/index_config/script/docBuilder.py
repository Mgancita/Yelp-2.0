# -*- coding: utf-8 -*-

import os
import xmltodict
import pickle
import re
from nltk.corpus import stopwords 

root_path = os.path.dirname(os.path.abspath( __file__ ))+"/../.."
data_path = root_path+"/index_config/data/"
documents_file="docs.dat"
index_file="{}.idx"
#set stopwords
en_stopwords=set(stopwords.words('english'))


class DataImport:
    
    def __init__(self,config):
        doc = config['dataConfig']['document']
        self.name=doc['@name']
        self.indexedFields=[]
        self.storedFields=[]
        self.multivalFields=[]
        self.columnTOField={}
        self.indexDir=root_path+doc['@indexDir']
        self.sql=doc['@sql']
        self.primarykey=None
        self.field_inverted_index={}
        
        
        for field in doc['field']:
            if '@indexed' in field:
                if field['@indexed'] == "true":
                    self.indexedFields.append(field['@name'])
                    self.field_inverted_index[field['@name']] ={}
            
            if '@stored' in field:
                if field['@stored'] == "true":
                    self.storedFields.append(field['@name'])
            
            if '@primary' in field:
                if field['@primary'] == "true":
                    self.primarykey = field['@name']
            
            
            if '@multivalField' in field:
                if field['@multivalField'] == "true":
                    self.multivalFields.append(field['@name'])
            
            self.columnTOField[field['@column']] = field['@name']            
        
    
    
    @staticmethod           
    def loadConfig(file):
        with open(file) as fd:
            conf = xmltodict.parse(fd.read())
            dIConfig = DataImport(conf)    
            return dIConfig
        
    def filter_stopwords(self,list):
        return [word for word in list if word not in en_stopwords]
    
    #preprocess string to retain only alphanumeric characters
    def preprocess_string(self,string):
        res_string=re.sub('[^a-zA-Z0-9\s+]+','',string)
        return res_string

    def preprocess_indexstr(self,idx,field,value):
        inverted_idx=self.field_inverted_index[field]
        string = self.preprocess_string(value)
        text = string.split()
        text =[ word.lower() for word in text]
        text = self.filter_stopwords(text)
        #de-duplicate
        text = list(set(text))
        for word in text:
            if word not in inverted_idx:
                inverted_idx[word] = []
                inverted_idx[word].append(idx)
            else:
                inverted_idx[word].append(idx)
        
    def addToIndex(self,idx,field,document):
        
        if type(document[field]).__name__ == 'str':
            self.preprocess_indexstr(idx,field,document[field])
        else:
            pass
        
    
    def index(self,idx,document):
        
        for field in self.indexedFields:
            self.addToIndex(idx,field,document)
    
    
    def indexFromDB(self,db):
        """Index from config and db"""
        cursor=db.connection.cursor().execute(self.sql)
        documents = {}
        
        for idx,row in enumerate(cursor):
            document={}
            for key,value in self.columnTOField.items():
                document[value]=row[key]
            #index with primary key
            self.index(document[self.primarykey],document)
            documents[document[self.primarykey]]=document
        
        #store documents
        docs_out = open(self.indexDir+documents_file,"wb")
        pickle.dump(documents, docs_out)
        docs_out.close()
        
        #pickle inverted indexes
        for field,inverted_index in self.field_inverted_index.items():
            idx_out = open(self.indexDir+index_file.format(field),"wb")
            pickle.dump(inverted_index, idx_out)
            idx_out.close()
        #docs_in = open(documents_file,"rb")
        #docs_dict = pickle.load(docs_in)
        #print(docs_dict)
        
        