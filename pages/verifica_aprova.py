import pandas as pd
import numpy as np
import streamlit as st
import pydeck as pdk
import re
from itertools import chain

#Configurações do Streamlit

st.set_page_config(page_title='Viabilidade ALF Itajaí', 
                   layout="centered", 
                   initial_sidebar_state='expanded',
                   page_icon=('./images/favicon.png'), 
                   menu_items=None
                   )

logo_image = ('./images/logo.png')

#Sidebar
st.sidebar.image(logo_image, width=150)
st.sidebar.divider()
st.sidebar.page_link("app.py", label="01_Consulta de Viabilidade (inscr.)")
st.sidebar.page_link("pages/cv_zona.py", label="__Consulta de Viabilidade (zona)")
st.sidebar.page_link("pages/verifica_aprova.py", label="02_Verifica processo ALF")
st.sidebar.page_link("pages/links.py", label="03_Links úteis")
st.sidebar.page_link("pages/documentacao-complementar-ALF.py", label="04_Doc. complementar ALF")
st.sidebar.page_link("pages/estudo-de-impacto-de-vizinhanca.py", label="05_EIV")


#Tabelas CSV

df_permissao=pd.read_csv("dados/permissao.csv", nrows=2000)
df_risco_uso=pd.read_csv("dados/risco_uso.csv", nrows=2000)
df_zona_col=pd.read_csv("dados/zona_col.csv", nrows=100)
df_inscricao=pd.read_csv("dados/inscricao.csv")

#Página principal do Streamlit - fixa
st.subheader('Consulta de Viabilidade - Alvará de Funcionamento - Itajaí')

col1, col2 = st.columns(2)

with col1:
    ib_zon = st.text_input(
    "Inscrição Imobiliária (Padrão 000.000.00.0000)",
    key="ib_iscricao"
    )

with col2:
    ib_area = st.number_input(
    "Área ocupada (m²)",
    key="ib_area"
    )

ib_cnpj = st.text_input(
    "Cole todo o texto do CNPJ - O programa irá selecionar as atividades de forma automática ",
    key="ib_cnpj"
    )

def clear_text():
    st.session_state["ib_cnpj"] = ""
    st.session_state["ib_area"] = 0
    st.session_state["ib_iscricao"] = ""
st.button("Limpar", on_click=clear_text)

st.divider()    

try:
    if ib_cnpj and ib_area and ib_zon != "":
        
        #Lista os cnaes do CNPJ
        cnaes_cnpj = re.findall(r'\d\d.\d\d-\d-\d\d', ib_cnpj)
        cnae_principal_cnpj=cnaes_cnpj[0]
        numero_cnpj = re.findall(r'\d\d.\d\d\d.\d\d\d/\d\d\d\d-\d\d', ib_cnpj)
        texto_cnpj_split = re.sub(' +', ' ',ib_cnpj).split(' ')


        #Filtra a coluna de risco em função da área
        if ib_area <= 150:
            id_risco='ate150.'
        if ib_area > 150 and ib_area <= 500:
            id_risco='150a500.'
        if ib_area > 500 and ib_area <= 750:
            id_risco='500a750.'
        if ib_area > 750:
            id_risco='acima750.'
        
        #Filta a coluna de uso em função da área
        if ib_area <= 150:
            id_uso='ate150'
        if ib_area > 150 and ib_area <= 200:
            id_uso='150a200'
        if ib_area > 200 and ib_area <= 500:
            id_uso='200a500'
        if ib_area > 500 and ib_area <= 750:
            id_uso='500a750'
        if ib_area > 750 and ib_area <= 1000:
