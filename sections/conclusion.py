import streamlit as st

from lib import load, viz

df = load.load_models()

st.title("Our answer")
st.write("TODO Student A : la reponse du groupe, en une phrase, avec les chiffres.")

st.subheader("What our data cannot show")
st.write(
    "TODO Student C : compute n'est pas du chiffre d'affaires ni des parts de marche. "
    "Donner le pourcentage de modeles dont le compute est connu, par annee."
)

viz.footer()
