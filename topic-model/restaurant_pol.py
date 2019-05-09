#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import ast
from collections import defaultdict
import pandas as pd


df = pd.read_csv("/Users/asnafatimaali/Documents/GitHub/Yelp-2.0/data/reviews_topics_polarity.csv", encoding = "utf-8")
#df.columns
new_df = df.loc[:,["resturant_id" ,"topic_senti"]] # df of restaurant ids and topic polarities from processed file in data folder

unique_restaurant = list(pd.unique(new_df["resturant_id"])) # get all the unique restauarant ids # 390 

#creates dictionary where keys are unique restaurant ids, and values are a grouped list of the topic / polarity dictionaries (output stores values as type string)
grouped_dict = new_df.groupby('resturant_id')['topic_senti'].apply(lambda x: x.tolist()).to_dict()  

new_dict= {}

for key, value in grouped_dict.items(): # create new dictionary same as above, but the values are type dictionaries, rather than type strings
    vals = []
    for x in value:
        new_vals = ast.literal_eval(x)
        vals.append(new_vals)
    new_dict[key] = vals
  

# Creates list of dictionaries, one for each unique restaurant id, where the keys are the topics and the values are
# a list of all the sentiment scores from all the reviews associated to that restaurant pertaining to the respective topic
# Since it's stored in a list, order is perserved in the order of restaurants read from the unique restaurant list
    
topic_polarity = []

for x in unique_restaurant:
    topic_pols = defaultdict(list)
    for dicts in new_dict[x]:
        for key, value in dicts.items():
            topic_pols[key].append(value)
    topic_pols = dict(topic_pols)
    topic_polarity.append(topic_pols)
    
#print(topic_polarity)
#len(topic_polarity)


# Takes the average of the list stored as a value. 
# output is stored in a format that is easy to use for our interface. 
average_polarity = []
for x in topic_polarity:
    temp_lst = []
    for y in x.keys():
        avg_pols = {}
        avg = round(sum(x[y]) / len(x[y]),2)
        avg_pols["name"] = y 
        avg_pols["polarity"] = avg
        temp_lst.append(avg_pols)
    average_polarity.append(temp_lst)

#print(average_polarity)
    
complete_df = pd.DataFrame()

complete_df["resturant_id"] = unique_restaurant
complete_df["average_polarity"] = average_polarity

complete_df.to_csv("/Users/asnafatimaali/Documents/GitHub/Yelp-2.0/data/restaurant_average_polarity.csv", index = False)