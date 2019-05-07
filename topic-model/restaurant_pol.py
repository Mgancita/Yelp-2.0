#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import ast
from collections import defaultdict
import pandas as pd


df = pd.read_csv("/Users/asnafatimaali/Documents/GitHub/Yelp-2.0/data/reviews_topics_polarity.csv", encoding = "utf-8")
#df.columns
new_df = df.loc[:,["resturant_id" ,"topic_senti"]]

unique_restaurant = list(pd.unique(new_df["resturant_id"]))

        
df['topic_senti'] = df['topic_senti'].apply(lambda x: ast.literal_eval(x))

grouped_dict = new_df.groupby('resturant_id')['topic_senti'].apply(lambda x: x.tolist()).to_dict()

new_dict= {}

for key, value in grouped_dict.items():
    vals = []
    for x in value:
        new_vals = ast.literal_eval(x)
        vals.append(new_vals)
    new_dict[key] = vals
  

topics_polarity = []
topic_polarity = []
counter = 0
for x in unique_restaurant:
    topic_pols = defaultdict(list)
    for dicts in new_dict[x]:
        for key, value in dicts.items():
            topic_pols[key].append(value)
    topic_pols = dict(topic_pols)
    topic_polarity.append(topic_pols)
    counter += 1

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


complete_df = pd.DataFrame()

complete_df["resturant_id"] = unique_restaurant
complete_df["average_polarity"] = average_polarity

complete_df.to_csv("/Users/asnafatimaali/Documents/GitHub/Yelp-2.0/data/restaurant_average_polarity.csv", index = False)