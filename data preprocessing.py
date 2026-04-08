import numpy as np
import pandas as pd

credits= pd.read_csv('tmdb_5000_credits.csv')
#print(credits.shape)
#print(credits.info())

movies= pd.read_csv('tmdb_5000_movies.csv')
#print(movies.shape)
#print(movies.info())


#here we have diffrent ie 2 datframes ao first of all we have to merge them
movies=movies.merge(credits,on='title')
#print(movies.shape)
#print(movies.info())

#here we have to make a extra copy of our datframe so at any issue we can use it
df=movies.copy()


# now we checked serieswise that which column is useful for us to create tags and other we have to remove them
# now i make a list of columns that can be useful
'''
1)genres
2)movies_id
3)keywords
4)title
5)overview
6)cast
7)crew
'''

movies=movies[['genres','movie_id','keywords','title','overview','cast','crew']]
#print(movies.head(5))
#print(movies.shape)

#here we checked that any columns contains null value or not
(movies.isnull().sum())

#here we checked our 'overview' column contains some 'nan' values so we have to remove them

movies.dropna(inplace=True)
(movies.isnull().sum())


#we also check for duplicated data
(movies.duplicated().sum())

# Now we have to create a new dataframe having columns as[id,title,tags]
# so we have to combines columns as genres,overview,cast,crew,keywords to make tag column
# Now first we work on genres column

(movies.iloc[0].genres) 
# [{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]

# we have to make in this form ie.[Action,Adventure,Fantasy,Science Fiction]
import ast

def convert(obj):
    list=[]
    for i in ast.literal_eval(obj):
        list.append(i['name'])
    return list

movies['genres']=movies['genres'].apply(convert)
#print(movies['genres'])


'''list=[]
for i in ([{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]
):
        list.append(i['name'])
        
print(list)'''        



movies['keywords']=movies['keywords'].apply(convert)
#print(movies['keywords'])


def convert3(obj):
    list=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            list.append(i['name'])
        else:
            break    
    return list

movies['cast']=movies['cast'].apply(convert3)
#print(movies['cast'])

#print(movies.head(5))




def fetch_director(obj):
    list=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            list.append(i['name'])
            break
    return list

movies['crew']=movies['crew'].apply(fetch_director)
#print(movies['crew'])


# here we have 'Overview' columnn in string format so we have to make it in list format so we can concatinate with other columns

movies['overview']=movies['overview'].str.split()
#print(movies['overview'])
#movies['overview']=movies['overview'].apply(lambda x: x.split())   // we can also use this

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])

#print(movies.head(10))

#creating a new column tags
movies['tags']=movies['genres']+movies['cast']+movies['crew']+movies['keywords']+movies['overview']

# creating a new dataframe
new_df=movies[['movie_id','title','tags']]
#print(new_df.head())

# we have to convert tags column dtype to string
#print(new_df['tags'].str.join(sep=" "))  // we can also use this
new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))
#print(new_df['tags'])


# we convert tas to lowercase as suggested
new_df['tags']=new_df['tags'].apply(lambda x: x.lower())


new_df.to_csv('cleaned data.csv',index=False)

