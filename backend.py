#==================SYSTEME DE RECOMMANDATION DE SITES DE E-LEARNING===============#
"""
Le but de ce systeme est de recommander quatre site de e-learning a l'utilisateur en fonction de ses criteres.

Boris Constantin Danmitondé
"""

#Importation des librairies
import pandas as pd
import numpy as np
from warnings import filterwarnings
filterwarnings('ignore')

#Chargement des donnees des sites de e-learning
df = pd.read_excel('Donnees/e-learning_sites.xlsx')
df.rename(columns={"Names min":"lower_names", "Languages":"languages"}, inplace=True)

#Selection des colonnes essentielles et preprocessing
data = df[['lower_names','courses','certificates','free_certif','discount','vid_text','languages','topics']]
data['topics'] = data['topics'].map(lambda x:x.replace(' ','').lower().split(','))


#extraction de tous les themes d'etudes du jeu de donnees
topics = list(df['topics'].values)
topics_list = [[i for i in topic.split(',')] for topic in topics]
topics_list = [[topic for topic in listes] for listes in topics_list]
topics_sublist = [topic for topic in topics_list if type(topic)==list] #sous-listes de themes
topics_sublist_splitted=[]
for liste in topics_sublist:
  for i in liste:
    topics_sublist_splitted.append(i)
topics_sublist_splitted = [elem.strip() for elem in topics_sublist_splitted]
for elem in topics_list:
  if type(elem)!=list and elem not in topics_sublist_splitted:
    topics_sublist_splitted.append(elem.lower().strip())
topics_sublist_splitted = [x for x in topics_sublist_splitted if  x != '']
final_topics_list = sorted(list(set(topics_sublist_splitted)))
final_topics_list = [topic.lower().replace(' ','') for topic in final_topics_list]


#Ici je cree un dictionnaire regroupant les sites par themes d'etudes
topic_dict = {}
for topic in final_topics_list:
  for index, row in data.iterrows():
    if topic in row['topics']:
      if topic in topic_dict:
        topic_dict[topic].append(row['lower_names'])
      else:
        topic_dict[topic] = [row['lower_names']]


#Nous transformons ce dictionnaire en dataframe de deux colonnes
sites_grouped_df = pd.DataFrame(list(topic_dict.items()), columns = ['topics','sites'])
sites_grouped_df['normal_sites_names'] = [[x.capitalize() for x in row['sites']] for index, row in sites_grouped_df.iterrows()]


#Modèle de recommandation :
#*************************
#Le modèle filtre en un premier temps un site qui offrent des cours dans les domaines sélectionnés
#par l'utilisateur puis utilise l'algorithme de similarité pour trouver d'autres sites similaires

def model(courses_topics, courses_type, need_certif, vid_text, languages, pay_certif='No', need_discount='No'):

  #j'instancie des variables pour donner des notes aux sites quand ils remplissent ou non les criteres de l'utilisateur
  courses_note, cert_note, pay_certif_note, vid_text_note, discount_note, languages_note = 0,0,0,0,0,0

  #je cree un dictionnaire qui comporte les themes d'etudes selectionnes par l'utilisateur associes aux sites qui
  #proposent ces cours
  sites_topic_dict= {}
  final_sites_weight = {}
  for topic in courses_topics:
    relatives_sites_set = set()
    for index, row in sites_grouped_df.iterrows():
      if topic == row['topics']:
        relatives_sites_set = relatives_sites_set | set(site for site in row['sites'])
        if topic in sites_topic_dict:
          sites_topic_dict[topic].append(list(relatives_sites_set))
        else:
          sites_topic_dict[topic] = list(relatives_sites_set)

  # un site peut apparaitre plus d'une fois dans le dictionnaire s'il couvre plus d'un cours demande par l'utilisateur
  # ici je trie les sites present dans le dictionnaire precedent et le nombre que chaque site apparait (son poids)
  sites_list = []
  sites_weight_dict = {}
  for value in sites_topic_dict.values():
    for site in value:
      sites_list.append(site)
  for site in set(sites_list):
    sites_weight_dict[site] = sites_list.count(site)

 #ici des points seront attribués à chaque site en fonction de son taux de correspondance aux preferences de l'utilisateur
  for index, row in data.iterrows():
    if row['lower_names'] in set(sites_weight_dict):
      if row['courses'] == courses_type: courses_note = 1
      if row['certificates'] == 'None' == need_certif :
        cert_note = 1
        pay_certif_note = 1
        discount_note = 1
      elif row['certificates'] == 'Yes' == need_certif:
        cert_note = 1
        if row['free_certif'] == 'No' != pay_certif:
          pay_certif_note=1
          if row['discount'] in ['Yes','Not All'] and need_discount == 'Yes' or row['discount'] == 'No' == need_discount:
            discount_note = 1
      if row['vid_text'] == vid_text : vid_text_note = 2
      if set(row['languages'].replace(' ','').split(',')) & set(language.replace(' ','') for language in languages) != {} :
        if set(row['languages'].replace(' ','').split(',')) & set(language.replace(' ','') for language in languages) == len(set(language.replace(' ','') for language in languages)):
          languages_note = 2
        else :
          languages_note = 1

      #ici le point total de chaque site sera calcule puis stocke dans le dictionnaire 'final_sites_weight'

      final_weight = sites_weight_dict[row['lower_names']] + sum([courses_note,cert_note,pay_certif_note,discount_note,vid_text_note,languages_note])
      final_sites_weight[row['lower_names']] = final_weight

  #a la sortie de la boucle, le dictionnaire 'final_sites_weight' comporte chaque site avec son poids total
  #ces poids sont utilises pour filtrer le site le mieux adapte dans la variable 'top_site'
  top_sites = [x[0].capitalize() for x in sorted(final_sites_weight.items(), key=lambda x : x[1], reverse=True)][:4]
  sites_links = [list(df[df['lower_names']==x.lower()]['url']) for x in top_sites]

  return top_sites, sites_links




#borisdanmitonde
