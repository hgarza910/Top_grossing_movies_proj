import pandas as pd
import numpy as np

#df = pd.read_csv("Top_grossing_movies.csv")
df =pd.read_csv('Top_grossing_movies_cleaned.csv', index_col=0)
#%%
# Fill in missing movies - sometimes api doesn't collect all movies
num_missing = df.isnull().sum()
num_missing
#%%
# gather movies still missing
missing_movies = df[df['Descriptions'].isnull()]
ids = missing_movies.Id
#%%
missing_movies.shape
#%%
# try to collect missing movie data again
from Data_collection import get_description, get_ratings, join_get_features, get_features, get_production_team, collect_imdb_info
from PyMovieDb import IMDB

imdb = IMDB()

missing_df = collect_imdb_info(ids)
#%%
# join missing moives back to original dataframe
missing_movies = missing_movies.dropna(axis=1, how='all')
missing_filled = missing_movies.join(missing_df.set_index(missing_movies.index))
df = df.fillna(missing_filled)
df.isnull().sum()
# Repeat collection of missing movies if necessary.

#%%

# set missing gross values as 0 since the movies were not shown in this region
df['Dom_gross'] = df['Dom_gross'].apply(lambda x: x.replace('-', '0'))
# turn gross into numeric types
df['Ww_gross'] = df['Ww_gross'].apply(lambda x: x.replace('$','').replace(',',''))
df['Ww_gross'] = pd.to_numeric(df['Ww_gross'])
df['Dom_gross'] = df['Dom_gross'].apply(lambda x: x.replace('$','').replace(',',''))
df['Dom_gross'] = pd.to_numeric(df['Dom_gross'])
df['Fore_gross'] = df['Fore_gross'].apply(lambda x: x.replace('$','').replace(',',''))
df['Fore_gross'] = pd.to_numeric(df['Fore_gross'])

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
gen = df['Genres'].apply(lambda x: str(x).replace('\n','').replace(' ','').replace(':[','').split(','))
df['Genres'] = gen
# now split genres into seperate columns
df[['Genre1','Genre2','Genre3']] = pd.DataFrame(df.Genres.tolist(), index=df.index)

# clean release date --- might want date to be an int instead of string
rel_date = df['Release'].str.strip()
rd = rel_date.str.split(':').str[1]
rd = rd.apply(lambda x: str(x).replace('"',''))
df['Release'] = rd
release = pd.to_datetime(df['Release'])
df['Release'] = release

# clean keywords
kw = df['Keywords'].str.split(':').str[1]
kw = kw.apply(lambda x: str(x).replace('"',''))
df['Keywords'] = kw

# clean runtime
rt = df['Runtime'].str.split(' "').str[2]
df['Runtime'] = [str(x).replace('PT','') for x in rt]

# clean actors
act = df['Actors'].str.split(',').apply(lambda x: x[::2] if type(x) == list else x)
act_fixed = [str(x).replace(' ','').replace('\\n','').replace('"name":','').replace(':[','').replace('{','').replace('\'','').replace('[','').replace(']','') for x in act]
df['Actors'] = act_fixed
# split actors into separate columns
df[['Actor1','Actor2','Actor3']] = df['Actors'].apply(lambda x: pd.Series(x.split(',')))

# clean directors
dir = df['Directors'].str.split(',').apply(lambda x: x[::2] if type(x) == list else x)
dir_fixed = [str(x).replace(' ','').replace('"name":','').replace('"director":','').replace('\n','').replace('\\n','').replace('\'','').replace('{','').replace('[','').replace(']','') for x in dir]
df['Directors'] = dir_fixed
# seperate Directors
df[['Director1','Director2','Director3']] = df['Directors'].apply(lambda x: pd.Series(x.split(',')))

# clean creators
cre = df['Creators'].str.split(',').apply(lambda x: x[::2] if type(x) == list else x)
cre_fixed = [str(x).replace(' ','').replace('"name":','').replace('"creator":','').replace('\n','').replace('\\n','').replace('\'','').replace('{','').replace('[','').replace(']','') for x in cre]
df['Creators'] = cre_fixed
# Separate Creators
df[['Creator1','Creator2','Creator3']] = df['Creators'].apply(lambda x: pd.Series(x.split(',')))

# Drop redundant columns
df = df.drop(columns=['Unnamed: 0','Genres','Actors','Directors','Creators'], axis=1)


#%%
df.dtypes
df.head()
#%%
df = df.drop(columns=['Unnamed: 0'], axis=1)
#%%
df.to_csv('Top_grossing_movies_cleaned.csv')
#%%
