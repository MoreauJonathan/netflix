#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 14:21:31 2020

@author: jonathan
"""
# 20. Créez un dataframe nommé « show_listed_in » ayant pour
# seul colonne « show_id » et « listed_in ».


import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://jonathan:Claus5991.@localhost:3306/netflix')

donnees = pd.read_csv('/home/jonathan/Documents/netflix_titles.csv')
print(donnees)
#####donnees.drop(donnees.columns[12],axis=1,inplace=True)

        
######Correction Anthony Jacquemin

#donnees = pd.read_csv("netflix_titles.csv") #à rectifier par le chemin où se trouve votre fichier

#Suppression des doublons (en fonction de toutes les colonnes sauf index)
# 1 ligne en moins
donnees = donnees.drop_duplicates(subset=donnees.columns[1:])

#Suppression des lignes ayant des valeurs indéfinies
# 2460 lignes en moins !!!!
donnees = donnees.dropna()

# On crée le DataFrame show_listed en précisant ses colonnes
# Il sera utilisé à la fin de la partie 3 pour remplir la table côté MySQL 
# qui fait la liaison entre le catalogue et les catégories
show_listed_in = pd.DataFrame(columns = ['sh_id','listed_in'])

# Pour chaque ligne (film ou série) i du DataFrame
for i in donnees.index:
    # On récupère toutes les catégories que l'on sépare dans une liste
    categoriesFilm = donnees["listed_in"][i].split(", ") 
    # On crée une liste de même longueur (len(categoriesFilm)) remplie par l'identifiant show_id
    # ex pour créer une liste : ["toto"] * 3 crée la liste ["toto, "toto", "toto"]
    idFilm = [donnees["sh_id"][i]] * len(categoriesFilm)
    # On crée un Dataframe df temporaire qui fusionne les 2 listes qu'on vient de créer
    df = pd.DataFrame({'sh_id': idFilm,'listed_in': categoriesFilm})
    # On colle ce Dataframe temporaire à show-listed_in
    show_listed_in = show_listed_in.append(df)
    
# show_listed_in contient tous les DataFrames temporaires qu'on a créés à chaque ligne       
show_listed_in 

###############################Correction Rafik

tmp2 = donnees.loc[donnees["listed_in"].notna()][['show_id', 'listed_in']]

show_listed_in = pd.DataFrame(columns = ['show_id', 'listed_in'])


for i in range(tmp2.shape[0]):
    tmp = tmp2.iloc[i]["listed_in"].split(", ")
    show_id = [tmp2.iloc[i]["show_id"]]*len(tmp)
    df = pd.DataFrame({'show_id': show_id,
                    'listed_in': tmp}, columns = ['show_id', 'listed_in'])
    show_listed_in = show_listed_in.append(df, ignore_index=True)



#21. Créez un dataframe nommé « listed_in » ayant pour co-
#lonne « listed_in_id » et « listed_in ».

################################Correction
listed_in = show_listed_in['listed_in'].drop_duplicates().reset_index(drop=True).reset_index()
listed_in = listed_in.rename(columns={"index": "listed_in_id"})
show_listed_in = show_listed_in.merge(listed_in,
                                      left_on='listed_in',
                                      right_on='listed_in',
                                      how='left')
del show_listed_in['listed_in']

##############################################
#22. Faire de même avec les colonnes director et cast en créant
#des dataframe qui leur sont dédier.

tmp2 = donnees.loc[donnees["director"].notna()][['show_id', 'director']]

show_director = pd.DataFrame(columns = ['show_id', 'director'])


for i in range(tmp2.shape[0]):
    tmp = tmp2.iloc[i]["director"].split(", ")
    show_id = [tmp2.iloc[i]["show_id"]]*len(tmp)
    df = pd.DataFrame({'show_id': show_id,
                    'director': tmp}, columns = ['show_id', 'director'])
    show_director = show_director.append(df, ignore_index=True)

director = show_director['director'].drop_duplicates().reset_index(drop=True).reset_index()
director = director.rename(columns={"index": "director_id"})
show_director = show_director.merge(director,
                                      left_on='director',
                                      right_on='director',
                                      how='left')

del show_director['director']

##################################################

tmp2 = donnees.loc[donnees["cast"].notna()][['show_id', 'cast']]

show_cast = pd.DataFrame(columns = ['show_id', 'cast'])


for i in range(tmp2.shape[0]):
    tmp = tmp2.iloc[i]["cast"].split(", ")
    show_id = [tmp2.iloc[i]["show_id"]]*len(tmp)
    df = pd.DataFrame({'show_id': show_id,
                    'cast': tmp}, columns = ['show_id', 'cast'])
    show_cast = show_cast.append(df, ignore_index=True)

cast = show_cast['cast'].drop_duplicates().reset_index(drop=True).reset_index()
cast = cast.rename(columns={"index": "cast_id"})
show_cast = show_cast.merge(cast,
                                      left_on='cast',
                                      right_on='cast',
                                      how='left')

del show_cast['cast']


donnees['duration'] = donnees['duration'].str.replace(" min", "").str.replace(" Season", "").str.replace(" season", "").str.replace("s", "").astype(int)
donnees['date']=pd.to_datetime(donnees['date'])



#insertion tables

donnees.to_sql('donnees', con=engine, if_exists='append', index=False)
country.to_sql('country', con=engine, if_exists='append', index=False)
cast.to_sql('cast', con=engine, if_exists='append', index=False)
director.to_sql('director', con=engine, if_exists='append', index=False)



#insertion tables d'association

country_catalogue.to_sql('country_catalogue', con=engine, if_exists='append', index=False)
cat_cast.to_sql('catalogue_cast', con=engine, if_exists='append', index=False)
director_catalogue.to_sql('director_catalogue', con=engine, if_exists='append', index=False)
catalogue_category.to_sql('catalogue_category', con=engine, if_exists='append', index=False)








