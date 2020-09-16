
import pandas as pd 
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://nouveau_utilisateur:mot_de_passe@localhost:3306/netflix')

df = pd.read_csv("/home/jonathan/Téléchargements/netflix_titles(1).csv")


#df=id/categorie
cat_name = pd.DataFrame(data = df,columns = ["ca_id", "cat_name"])
cat_name.dropna(inplace=True)


#df=id/cast
cast = pd.DataFrame(data = df,columns = ["ca_id", "cast_name"])

cast.dropna(inplace=True)
print(cast)

#df=id/director
directors = pd.DataFrame(data = df,columns = ["ca_id", "dir_name"])
directors.dropna(inplace=True)

#df=id/country
country = pd.DataFrame(data = df,columns = ["ca_id", "co_name"])
country.dropna(inplace=True)

#fonction split 
def separator(id, column, column_name):
    c = 0
    liste_id = []
    liste_col = []
    for i in column:
        x = i.split(", ")
        for z in x:
            liste_col.append(z)
            liste_id.append(id[c])
        
        c+=1
    dataframe = pd.DataFrame({'ca_id':liste_id, column_name: liste_col}, columns = ['ca_id', column_name])
    return dataframe 





#dataframe id/catégories
cat_id=separator(cat_name['ca_id'], cat_name['cat_name'], 'cat_name')
#dataframe id/cast
cast_id=separator(cat_name['ca_id'], cast['cast_name'], 'cast_name')
#dataframe id/directors
dir_id=separator(cat_name['ca_id'], directors['dir_name'], 'dir_name')
#dataframe id/country
country_id=separator(cat_name['ca_id'], country['co_name'], 'co_name')


def table(df, column ,id): #formatage table
    data = df.drop_duplicates(subset=[column]).reset_index().rename(columns={"index": id})
    del data['ca_id']
    print(data)
    return data

def associationTable(df_base, df, column ,id): #formatage table association
    data= df.merge(df_base, left_on=column, right_on= column)
    data = data.rename(columns={"ca_id_x": "ca_id"})
    del data[column]
    print(data)
    return data


#table categorie catalogue
categories = table(cat_id, "cat_name", "cat_id")
cat_categories = associationTable(categories, cat_id, "cat_name", "cat_id")

#table country catalogue
country = table(country_id, "co_name", "co_id")
cat_country = associationTable(country, country_id, "co_name", "co_id")

#table cast catalogue
cast = table(cast_id, "cast_name", "cast_id")
cat_cast = associationTable(cast, cast_id, "cast_name", "cast_id")

#table dir catalogue

dir = table(dir_id, "dir_name", "dir_id")
cat_dir = associationTable(dir, dir_id, "dir_name", "dir_id")


#table catalogue
del df['cat_name']
del df['dir_name']
del df['cast_name']
del df['co_name']
del df['Unnamed: 12']



#changement type durée et date ajout

df['ca_duration'] = df['ca_duration'].str.replace(" min", "").str.replace(" Season", "").str.replace(" season", "").str.replace("s", "").astype(int)
df['ca_date']=pd.to_datetime(df['ca_date'])



#insertion tables

df.to_sql('catalogue', con=engine, if_exists='append', index=False)
country.to_sql('country', con=engine, if_exists='append', index=False)
cast.to_sql('cast', con=engine, if_exists='append', index=False)
dir.to_sql('directors', con=engine, if_exists='append', index=False)
categories.to_sql('category', con=engine, if_exists='append', index=False)


#insertion tables d'association

cat_country.to_sql('catalogue_country', con=engine, if_exists='append', index=False)
cat_cast.to_sql('catalogue_cast', con=engine, if_exists='append', index=False)
cat_dir.to_sql('catalogue_directors', con=engine, if_exists='append', index=False)
cat_categories.to_sql('catalogue_category', con=engine, if_exists='append', index=False)







