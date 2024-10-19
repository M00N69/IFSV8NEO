import streamlit as st

# Configuration de la page en mode large
st.set_page_config(layout="wide")

# Titre principal
st.title("Extracteur de données du formulaire IFS NEO")

# Ajouter les différentes versions du projet avec des explications
st.subheader("Choisissez la version du projet")
version_projet = st.radio(
    "Sélectionnez la version du projet que vous souhaitez explorer :",
    ('Rapport IFS V8 (ifsv8.py)', 'Extraction NEO (neoextract.py)')
)

# Expander pour expliquer le fonctionnement du code
with st.expander("Explication des fonctionnalités du code"):
    st.write("""
    ### Rapport IFS V8 (ifsv8.py) :
    Cette version vous permet de télécharger un fichier JSON (.ifs), de le "dénormaliser" pour extraire des champs spécifiques, et de présenter les résultats dans un tableau propre. Vous pouvez également télécharger les données extraites sous forme de fichier Excel.
    
    ### Extraction NEO (neoextract.py) :
    Cette version offre des fonctionnalités similaires, avec des options supplémentaires pour filtrer les données via un système de UUID et personnaliser l'extraction des données. Vous pouvez aussi éditer les données extraites avant de les télécharger.
    """)

# Rendu conditionnel des pages en fonction de la sélection
if version_projet == 'Rapport IFS V8 (ifsv8.py)':
    st.write("Vous avez sélectionné la version **Rapport IFS V8**.")
    # Inclure le contenu de la version ifsv8.py ici
    # Par exemple : afficher le contenu de ifsv8.py
    # st.write(ifsv8_code_function()) <- Appel à une fonction du fichier ifsv8.py
    
elif version_projet == 'Extraction NEO (neoextract.py)':
    st.write("Vous avez sélectionné la version **Extraction NEO**.")
    # Inclure le contenu de la version neoextract.py ici
    # Par exemple : afficher le contenu de neoextract.py
    # st.write(neoextract_code_function()) <- Appel à une fonction du fichier neoextract.py
