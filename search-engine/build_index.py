# -*- coding: utf-8 -*-

from index_config.script.docBuilder import DataImport
from dataload.script.yelpdb import Database
import os

script_path = os.path.dirname(os.path.abspath( __file__ ))



db = Database.init(script_path+'/dataload/config/dataload-env.xml')
data_import = DataImport.loadConfig(script_path+'/index_config/config/dataimport.xml')

data_import.indexFromDB(db)

#rows=db.query(config.sql)

#print(rows)
