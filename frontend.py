#==================SYSTEME DE RECOMMANDATION DE SITES DE E-LEARNING===============#

"""
Le but de ce systeme est de recommander au plus quatre sites de e-learning a l'utilisateur en fonction de
ses criteres.
"""

#Importation des librairies
import pandas as pd
#import numpy as np
from warnings import filterwarnings
filterwarnings('ignore')
import streamlit as st
from warnings import filterwarnings
filterwarnings('ignore')
from backend import *


def main():
    st.title("e-Learning web sites recommender")
    st.subheader('''Welcome to this app
    We are going to recommend you e-learning web sites based on your choices
    and preferences. Select your choices, then click on 'Submit' button below to get recommendations !''')

    frontend_topics_list = [topic.upper() for topic in final_topics_list]
    courses_type = [value for value in list(data['courses'].value_counts().index)]
    need_certif = [value for value in list(data['certificates'].value_counts().index)]
    vid_text = [value for value in list(data['vid_text'].value_counts().index)]
    languages = ['English','French','Spanish','Deutch']
    pay_certif = ['Yes','No']
    need_discount = ['Yes','No']

    with st.form("users_preferences"):
        user_topics = st.sidebar.multiselect("Select your learning topics", frontend_topics_list)
        user_courses_type = st.sidebar.selectbox("Which type of courses do you want?",courses_type)
        user_vid_text = st.sidebar.selectbox("Do you prefer video courses or text?",vid_text)
        user_languages = st.sidebar.multiselect("In which languages do you want to learn?",languages)
        user_need_certif = st.sidebar.selectbox("Do you need courses certification?",need_certif)
        user_pay_certif = ''
        user_need_discount = ''
        if user_need_certif == 'Yes':
            user_pay_certif = st.sidebar.selectbox("Would you pay for certificates?",pay_certif)
            if user_pay_certif == 'Yes':
                user_need_discount = st.sidebar.selectbox("Would you like to get some discount on certificates prices?",need_discount)

        submitted = st.form_submit_button(label='Submit')


        recommendations=''
        if submitted :
            recommendations, links = model([x.lower() for x in user_topics],
                                            user_courses_type,
                                            user_need_certif,
                                            user_vid_text,
                                            languages,
                                            user_pay_certif,
                                            user_need_discount)

            for site, link in zip(recommendations, links):
                st.image(f'Donnees/sites logo/{site.lower()}.png')
                st.link_button(site, link)




if __name__ == "__main__":
    main()


#borisdanmitonde
