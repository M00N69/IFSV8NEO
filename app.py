import streamlit as st

# Configuration de la page en mode large
st.set_page_config(layout="wide")

# Initialisation de l'état de la session pour suivre la navigation
if "page" not in st.session_state:
    st.session_state.page = "home"  # La page par défaut est la page d'accueil

# Fonction pour changer de page
def navigate_to_page(page):
    st.session_state.page = page

# Titre principal
st.title("Extracteur de données du formulaire IFS NEO")

# Si l'utilisateur est sur la page d'accueil
if st.session_state.page == "home":
    # Ajouter les différentes versions du projet avec des explications
    st.subheader("Choisissez la version du projet")
    version_projet = st.radio(
        "Sélectionnez la version du projet que vous souhaitez explorer :",
        ('Rapport IFS V8 (ifsv8.py)', 'Extraction NEO (neoextract.py)')
    )

    # Expander pour expliquer le fonctionnement général
    with st.expander("Explication des fonctionnalités générales"):
        st.write("""
        Ce projet est conçu pour extraire des informations depuis des fichiers JSON issus des audits IFS. 
        Les deux versions de projet suivantes sont disponibles :
        
        - **Rapport IFS V8** : Extraction des données spécifiques d'un fichier JSON lié à un audit IFS V8.
        - **Extraction NEO** : Version avancée avec filtrage et modification des données extraites.
        """)

    # Expander explicatif pour chaque version
    if version_projet == 'Rapport IFS V8 (ifsv8.py)':
        with st.expander("Explication des fonctionnalités de la version Rapport IFS V8"):
            st.write("""
            Cette version permet d'extraire des informations spécifiques du fichier JSON lié à un audit IFS V8, telles que le nom du site audité, 
            le N° COID, l'adresse, etc. Vous pouvez également télécharger les données extraites sous forme de fichier Excel.
            """)
        
        # Bouton pour aller à la page IFS V8
        if st.button("Aller à la version Rapport IFS V8"):
            navigate_to_page("ifsv8")  # Redirige vers la page IFS V8

    elif version_projet == 'Extraction NEO (neoextract.py)':
        with st.expander("Explication des fonctionnalités de la version Extraction NEO"):
            st.write("""
            Cette version avancée permet d'extraire et de filtrer des données depuis les fichiers JSON liés aux audits IFS NEO, 
            avec possibilité de modifier les données avant téléchargement.
            """)
        
        # Bouton pour aller à la page NEO Extract
        if st.button("Aller à la version Extraction NEO"):
            navigate_to_page("neoextract")  # Redirige vers la page NEO Extract

# Si l'utilisateur est sur la page IFS V8
elif st.session_state.page == "ifsv8":
    st.header("Rapport IFS V8")
    st.write("Vous êtes sur la page du **Rapport IFS V8**.")
    # Appel de la fonction ou inclusion du contenu spécifique à la version IFS V8
    # Exemple : ifsv8_page_function()
    if st.button("Retour à la page d'accueil"):
        navigate_to_page("home")  # Retour à l'accueil

# Si l'utilisateur est sur la page NEO Extract
elif st.session_state.page == "neoextract":
    st.header("Extraction NEO")
    st.write("Vous êtes sur la page de **l'Extraction NEO**.")
    # Appel de la fonction ou inclusion du contenu spécifique à la version NEO Extract
    # Exemple : neoextract_page_function()
    if st.button("Retour à la page d'accueil"):
        navigate_to_page("home")  # Retour à l'accueil
