import numpy as np
import pandas as pd
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


df=pd.read_csv('cleaned data.csv')
ps=PorterStemmer()

def stem(text):
    list=[]
    for i in text.split():
        list.append(ps.stem(i))
    return " ".join(list)

df['tags']=df['tags'].apply(stem)  
#print(df['tags'])  


cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(df['tags']).toarray()
#print(vectors[0])
#print(vectors.shape)

similarity=cosine_similarity(vectors)
#print(similarity[0])

def recommend(movies):
    movie_index=df[df['title']== movies].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in movies_list:
        return df.iloc[i[0]].title
                       
#recommend('Batman Begins')
#print(df.head())



pickle.dump(df.to_dict(),open('movies_dict.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))