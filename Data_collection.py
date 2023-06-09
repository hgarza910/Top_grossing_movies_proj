import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from PyMovieDb import IMDB


#%%
# collect box office gross for movies

def get_id(title):
    a, b = title.split("/title/")
    id, n = b.split("/")
    return id

pg = 0
ids = []
titles = []
ww_gross = []
dom_gross = []
fore_gross = []
years = []

while pg != 1000:
    url = f'https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?area=XWW&offset={pg}'
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    title = soup.find_all('td', class_='a-text-left mojo-field-type-title')
    gross = soup.find_all('td', class_='a-text-right mojo-field-type-money')
    year = soup.find_all('td', class_='a-text-left mojo-field-type-year')

    for t in title:
        mov = t.find('a')['href']
        id = get_id(mov)
        ids.append(id)
        titles.append(t.select('a')[0].string)
    for y in year:
        if len(y.select('a')) == 1:
            years.append(y.select('a')[0].string)
        else:
            years.append(y.string)
    i = 0
    for g in gross:
        if i % 3 == 0:
            ww_gross.append(g.string)
        elif i % 3 == 1:
            dom_gross.append(g.string)
        else:
            fore_gross.append(g.string)
        i += 1

    pg += 200

gross_dict = {'Id': ids, 'Title': titles, 'Ww_gross': ww_gross, 'Dom_gross': dom_gross, 'Fore_gross': fore_gross, 'Year': years}
mojo_df = pd.DataFrame(gross_dict)
#%%
mojo_df.to_csv('Mojo_df.csv')
mojo_df.head(10)
#%%
# collect details and information on movies for imdb
imdb = IMDB()

descriptions = []
rating_count = []
rating_value = []
best_rating = []
worst_rating = []
content_rating = []
genres = []
release_date = []
keywords = []
runtime = []
actors = []
directors = []
creators = []

def get_description(details):
    overview = details[0]
    desc = ''
    x = overview.split('"review"')
    if len(x) == 2:
        general, review = overview.split('"review"')
        junk, desc = general.split('description')
    else:
        desc = 'null'
    return desc

def get_ratings(details):
    rate_count, best_rate, worst_rate, rate_value = '','','',''
    if len(details) <= 1:
        rate_count, best_rate, worst_rate, rate_value = 'null', 'null', 'null', 'null'
    else:
        ratings = details[1]
        #print(ratings)
        rate_count, best_rate, worst_rate, rate_value = ratings.split(',')

    return rate_count, best_rate, worst_rate, rate_value

def join_get_features(details):
    cont_rate, genre, release, keywrds, rt, actor, director, creator = '', '', '', '', '', '', '', ''
    del details[:2]
    details = '},'.join(details)
    x = details.split('"actor"')
    #print(len(x))
    if len(x) <= 1:
        #print(x)
        cont_rate, genre, release, keywrds, rt, actor, director, creator = 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null'
    elif len(x) == 2:
        feats, team = details.split('"actor"')
        cont_rate, genre, release, keywrds, rt = get_features(feats)
        actor, director, creator = get_production_team(team)
    else:
        print("x longer than 2")
        print(x)
    return cont_rate, genre, release, keywrds, rt, actor, director, creator

def get_features(feats):
    release, keywrds, rt, z = '','','',''
    content, variety = feats.split('],')
    cont_rate, genre = content.split('"genre"')
    x = variety.split('",')
    if len(x) == 4:
        release, keywrds, rt, z = variety.split('",')
    elif len(x) == 3:
        release, keywrds, rt = variety.split('",')
    else:
        print(len(x))
        print(x)
    return cont_rate, genre, release, keywrds, rt

def get_production_team(team):
    actor, director, creator = team.split('],')
    return actor, director, creator

#%%
def collect_imdb_info(ids):
    descriptions = []
    rating_count = []
    rating_value = []
    best_rating = []
    worst_rating = []
    content_rating = []
    genres = []
    release_date = []
    keywords = []
    runtime = []
    actors = []
    directors = []
    creators = []

    for id in ids:
        print(id)
        movie = imdb.get_by_id(id)
        details = movie.split('},')

        description = get_description(details)
        rate_count, best_rate, worst_rate, rate_value = get_ratings(details)
        cont_rate, genre, release, keywrds, rt, actor, director, creator = join_get_features(details)

        descriptions.append(description)
        rating_count.append(rate_count)
        best_rating.append(best_rate)
        worst_rating.append(worst_rate)
        rating_value.append(rate_value)
        content_rating.append(cont_rate)
        genres.append(genre)
        release_date.append(release)
        keywords.append(keywrds)
        runtime.append(rt)
        actors.append(actor)
        directors.append(director)
        creators.append(creator)
    info_dict = {'Descriptions': descriptions, 'Rating_cnt': rating_count, 'Best_rating': best_rating, 'Worst_rating': worst_rating, 'Rating_value':rating_value, 'Content_rating':content_rating, 'Genres':genres, 'Release': release_date,
                 'Keywords': keywords, 'Runtime': runtime, 'Actors': actors, 'Directors': directors, 'Creators': creators}
    imdb_df = pd.DataFrame(info_dict)
    return imdb_df

'''
#imdb_df.to_csv('IMDB_df.csv')
#%%
desc_dict = {'Descriptions': descriptions}
imdb_desc = pd.DataFrame(desc_dict)
#%%
imdb_desc.to_csv('IMDB_descriptions.csv')
imdb_desc.head(1)
#%%
imdb_df.head()
#%%


# clean csv and then combine
#%%
df1 = pd.read_csv('IMDB_df.csv')
#%%
df1.head()
#%%
dict = {'Id': ids, 'Title': titles, 'Ww_gross': ww_gross, 'Dom_gross': dom_gross, 'Fore_gross': fore_gross,
        'Year': years, 'Descriptions': descriptions, 'Rating_cnt': rating_count, 'Best_rating': best_rating,
        'Worst_rating': worst_rating, 'Rating_value': rating_value, 'Content_rating':content_rating, 'Genres':genres,
        'Release': release_date, 'Keywords': keywords, 'Runtime': runtime, 'Actors': actors, 'Directors': directors,
        'Creators': creators
        }
df = pd.DataFrame(dict)
#%%
df.to_csv("Top_grossing_movies.csv")

#%%
movie = imdb.get_by_id('tt2109248')
#%%
df = pd.read_csv('Top_grossing_movies.csv')
missing = df[df['Descriptions'].isnull() ]
#%%
id2 = missing['Id']
#%%
info_dict = {'Descriptions': descriptions, 'Rating_cnt': rating_count, 'Best_rating': best_rating, 'Worst_rating': worst_rating, 'Rating_value':rating_value, 'Content_rating':content_rating, 'Genres':genres, 'Release': release_date,
             'Keywords': keywords, 'Runtime': runtime, 'Actors': actors, 'Directors': directors, 'Creators': creators}
imdb_missing_df = pd.DataFrame(info_dict)
#%%
# df is messed up bc of indexing
imdb_fixed = pd.DataFrame(data=imdb_missing_df)
#%%
imdb_fixed['Descriptions'] = imdb_missing_df['Descriptions']
#%%
'''