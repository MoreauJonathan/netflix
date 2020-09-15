#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 11:28:06 2020

@author: jonathan
"""

#Netflix
#1.Lire le fichier

import pandas as pd
dataframe = pd.read_csv('/home/jonathan/Documents/Simplon/2.Python/Exo Python/Netflix/434238_901459_compressed_netflix_titles.csv/netflix_titles.csv'
                        ,index_col = 0)
print(dataframe.head())

#2.Afficher les dimensions du dataframe

print(dataframe.shape)

#3.Compter les films et les séries

NbrMovie = dataframe.loc[dataframe['type']=='Movie'].type.value_counts()
print(NbrMovie)
NbrTVShow = dataframe.loc[dataframe['type']=='TV Show'].type.value_counts()
print(NbrTVShow)

#4.Générer le résumé statistique du dataframe

print(dataframe.describe(include='all'))
a= dataframe.describe(include='all')
#5.Compter les valeurs manquantes

print(dataframe.isna().sum())

#6.Explorer les valeurs manquantes
#a. Sur la colonne des directeurs de production

VMdirector = dataframe.loc[dataframe['director'].isna()]
print(VMdirector.type.value_counts())
Movie = VMdirector.loc[dataframe['type']=='Movie'].type.value_counts()
print(Movie)
TVShow = VMdirector.loc[dataframe['type']=='TV Show'].type.value_counts()
print(TVShow)

#b.Sur la colonne des acteurs

Cast = dataframe.loc[dataframe['cast'].isna()]
print(Cast)
print(Cast.listed_in.value_counts().head(10))

#7. Supprimer les lignes dupliquées

dup = dataframe.duplicated()
print(dup.value_counts())
drop = dataframe.drop_duplicates()
print(drop)

#8. Compter les films/séries produits par les États-Unis et par la France

France = dataframe[(dataframe["country"]=="France")]
print(France)
US = dataframe[(dataframe["country"]=="United States")]
print(US)
print(France.shape, US.shape)

#9. Afficher le contenu le plus vieux disponible sur Netflix

annee = dataframe.release_year.min()
print(annee)
ligne = dataframe['title'][(dataframe["release_year"]==annee)]
print(ligne)

#10. Afficher le film avec la durée la plus longue sur Netflix

MOVIE = dataframe.loc[dataframe['type']=="Movie"]
print(MOVIE)
duree = MOVIE.duration.str.replace(" min","").astype(int).sort_values(ascending=False).head(5)
print(duree)
print(pd.Series(MOVIE.duration).str.replace(" min","").astype(int).sort_values(ascending=False))

#Correction Raph

#8. Compter les films/séries produits par les États-Unis et par la France
data_film_usa = data.loc[data.country == 'United States', 'title']
data_film_fr = data.loc[data.country == 'France', 'title']
print(data_film_usa.shape[0])

#9. Afficher le contenu le plus vieux disponible sur Netflix
data_older = data.loc[data.release_year == data.release_year.min(), ['title', 'release_year']]
print(data_older)

#10. Afficher le film avec la durée la plus longue sur Netflix
#Afficher les 5 films les + long(juste la durée)
data_movies = data.loc[data.type == 'Movie']
duree = pd.Series(data_movies['duration']).str.replace(" min", "").astype('int').sort_values(ascending=False).head(5)
print(duree)

#Affiche les 5 films avec toutes les infos(version merge & series)
data_movies = data.loc[data.type == 'Movie']
duree = pd.Series(data_movies['duration']).str.replace(" min", "").astype('int').sort_values(ascending=False).head(5)
data_merged = pd.merge(data, duree.to_frame(), on='show_id', how='inner')
data_film_duration = data_merged.sort_values(by='duration_x', ascending=False).head(5)[["title", "duration_x"]]
print(data_film_duration)

#Affiche les 5 films avec toutes les infos
data["duration"] = pd.Series(data_movies['duration']).str.replace(" min", "").astype('int')
data_film_duration_2 = data.sort_values(by='duration', ascending=False).head(5)[["title", "duration"]]
print(data_film_duration_2)


##################################Netflix 2ème partie

#12. Afficher les directeurs qui ont produit le plus de films/sé-ries disponibles sur Netflix

import pandas as pd
import seaborn as sns
donnees=pd.read_csv('/home/jonathan/Documents/Simplon/2.Python/Exo Python/Netflix/434238_901459_compressed_netflix_titles.csv/netflix_titles.csv',
index_col=[0])
donnees["director"]

#13. Voir si Jan Suter travaille souvent avec les mêmes acteurs

donnees_jan_suter = donnees[donnees["director"].notna()]
jan_suter = donnees_jan_suter[donnees_jan_suter["director"].str.contains("Jan Suter")]
print(jan_suter)
jan_suter=pd.Series(", ".join(donnees_jan_suter["cast"].dropna()).split(', '))
jan_suter.value_counts().head(5)

#14. Représenter les dix pays qui ont produit le plus de contenus disponibles
#sur Netflix, avec le nombre de contenus par pays

pays = donnees.loc[donnees['country'].notna()]
print(pays)
top = pd.Series(','.join(pays['country']).split(','))
top = top.value_counts().head(10)
print(top)
topPays = pays[pays['country'].isin(top.index)]
print(topPays)

sns.set_style("darkgrid")
sns.countplot(data = topPays,x = 'country')
