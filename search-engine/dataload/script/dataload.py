# -*- coding: utf-8 -*-

from entity import Entity

from yelpdb import Database



db = Database.init('../config/dataload-env.xml')
entities = Entity.loadConfig('../config/dataload.xml')
for entity in entities:
    #print(entity.name)
    db.load(entity,True)


