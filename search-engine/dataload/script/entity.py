# -*- coding: utf-8 -*-
import xmltodict
import pandas as pd


class Entity: 
    
    def __init__(self,entity):
        self.name = entity['@name']
        self.loadOrder = entity['@loadOrder']
        self.source = entity['@source']
        self.fieldToColumn={}
        for field in entity['field']:
            self.fieldToColumn[field['@name']] = field['@column']
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
