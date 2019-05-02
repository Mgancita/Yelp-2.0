# -*- coding: utf-8 -*-
import xmltodict
import sqlite3
from sqlite3 import Error

class Database:
    @classmethod
    def create_connection(self,source):
        try:
            connection = sqlite3.connect(source)
            return connection
        except Error as e:
            print(e)
            
        return None
    
    
    def __init__(self,config):
        self.source = config['@source']
        self.type = config['@type']
        self.connection = self.create_connection(self.source)
        
    @staticmethod           
    def init(file):
        with open(file) as fd:
            doc = xmltodict.parse(fd.read())
            return Database(doc['dataloadEnv']['datasource'])
    
    def insert(self,entity):
        columns = []
        fields = []
        param_phold=[]
        for key,value in entity.fieldToColumn.items():
            columns.append(value)
            fields.append(key)
            param_phold.append('?')
        
        param = (str(param_phold)[1:-1]).replace("'","")
        sql_insert='INSERT OR IGNORE INTO {} ({}) VALUES({})'.format(entity.name,str(columns)[1:-1],param)
        value_list =[]
        for idx,row in entity.df.iterrows():
            values=[]
            for field in fields:
                values.append(row[field])
        
            value_list.append(tuple(values));
        try:
            self.connection.cursor().executemany(sql_insert,value_list)
            self.connection.commit();
        except Error as e:
            print(e)
        
    def load(self,entity,reset):
        """ This method takes argument entity and reset table flag(reset True will delete all the current data in db)"""
        if reset == True:
            print("deleting {}".format(entity.name))
            delete_sql_string = "DELETE FROM {}".format(entity.name)
            self.connection.execute(delete_sql_string)
            self.connection.commit();
        self.insert(entity)
        