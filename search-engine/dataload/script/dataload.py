# -*- coding: utf-8 -*-

from entity import Entity

from yelpdb import Database
import os

root_path = os.path.dirname(os.path.abspath( __file__ ))+"/../.."


db = Database.init(root_path+'/dataload/config/dataload-env.xml')
entities = Entity.loadConfig(root_path+'/dataload/config/dataload.xml')
for entity in entities:
    #print(entity.name)
    db.load(entity,True)


