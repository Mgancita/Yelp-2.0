# -*- coding: utf-8 -*-
import xmltodict
import os
import pandas as pd

root_path = os.path.dirname(os.path.abspath( __file__ ))+"/../.."

class Entity: 
    
    def __init__(self,entity):
        self.name = entity['@name']
        self.loadOrder = entity['@loadOrder']
        self.source = root_path+entity['@source']
        self.fieldToColumn={}
        for field in entity['field']:
            self.fieldToColumn[field['@name']] = field['@column']
        
        self.topicFieldColumn=None
        self.topicFieldToColumn={}
        if 'topicField' in entity:
            self.topicFieldColumn=entity['topicField']['@name']
            for topicField in entity['topicField']['topic']:
                 self.topicFieldToColumn[topicField['@name']] = topicField['@column']
                
        self.df = pd.read_csv(self.source)
    
    @staticmethod           
    def loadConfig(file):
        entities = []
        with open(file) as fd:
            doc = xmltodict.parse(fd.read())
            for entity in doc['dataloadMapper']['table']:
                table = Entity(entity)
                entities.append(table)
        return entities
