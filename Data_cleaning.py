import pandas as pd
import numpy as np

df = pd.read_csv("Top_grossing_movies.csv")

#%%
df.head()
#%%
df.dtypes
#lets drop descriptions?
df = df.drop("Descriptions", axis=1)
# clean rating_count
rate_count = df['Rating_cnt'].str.split('"ratingCount":').str[1]
df['Rating_cnt'] = rate_count.astype('Int64')
# clean best rating
best_rate = df['Best_rating'].str.split(':').str[1]
df['Best_rating'] = best_rate.astype('Int64')
# clean worst rating
worst_rate = df['Worst_rating'].str.split(':').str[1]
df['Worst_rating'] = worst_rate.astype('Int64')
# clean rating value
rate_value = df['Rating_value'].str.split(':').str[1]
rv = rate_value.str.strip()
df['Rating_value'] = rv.astype('float')
# clean content rating
content_rate = df['Content_rating'].str.split(':').str[1]
cr = content_rate.str.strip()
cr = cr.apply(lambda x: str(x).replace(',','').replace('"',''))
df['Content_rating'] = cr
# clean genres

# clean release date --- might want date to be an int instead of string
rel_date = df['Release'].str.strip()
rd = rel_date.str.split(':').str[1]
rd = rd.apply(lambda x: str(x).replace('"',''))
df['Release'] = rd
# clean keywords
#kw = df['Keywords'].str.split(' "').str[2]
kw = df['Keywords'].str.split(':').str[1]
kw = kw.apply(lambda x: str(x).replace('"',''))
df['Keywords'] = kw
# clean runtime
rt = df['Runtime'].str.split(' "').str[2]
df['Runtime'] = rt
# clean actors
act = df['Actors'].str.split(',')
at = act.apply(lambda x: x if )
# clean directors
# clean creators

# fill in nulls

#%%
