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

# Expander pour expliquer le fonctionnement général
with st.expander("Explication des fonctionnalités générales"):
    st.write("""
    Ce projet est conçu pour extraire des informations depuis des fichiers JSON issus des audits IFS. Il permet de dénormaliser les structures complexes de ces fichiers pour extraire des données spécifiques et les afficher sous forme de tableau.
    Les deux versions de projet suivantes sont disponibles :
    
    - **Rapport IFS V8** : Cette version extrait des données spécifiques d'un fichier JSON lié à un audit IFS V8.
    - **Extraction NEO** : Une version avancée avec des options supplémentaires pour filtrer et modifier les données extraites.
    """)

# Détail explicatif pour chaque version en fonction du choix de l'utilisateur
if version_projet == 'Rapport IFS V8 (ifsv8.py)':
    # Expander explicatif pour IFS V8
    with st.expander("Explication des fonctionnalités de la version Rapport IFS V8"):
        st.write("""
        ### Rapport IFS V8 :
        Cette version permet d'extraire des informations spécifiques du fichier JSON lié à un audit IFS V8, telles que :
        - Nom du site audité
        - N° COID du portail
        - Code GLN
        - Adresse, Ville, Pays, Code postal
        - Informations sur les sous-traitances et exclusions de produits
        
        **Fonctionnalités principales** :
        - Chargement d'un fichier JSON IFS V8
        - Extraction des données d'audit dans un tableau lisible
        - Téléchargement des données extraites au format Excel
        - Aucun traitement ou édition des données directement sur l'application
        """)

    # Bouton pour naviguer vers la page IFS V8
    if st.button("Aller à la version Rapport IFS V8"):
        st.write("Redirection vers la version **Rapport IFS V8**...")
        # Insérer le contenu de la page ifsv8.py ici
        # Exemple : st.write(ifsv8_page_function())

elif version_projet == 'Extraction NEO (neoextract.py)':
    # Expander explicatif pour NEO Extract
    with st.expander("Explication des fonctionnalités de la version Extraction NEO"):
        st.write("""
        ### Extraction NEO :
        Cette version avancée permet d'extraire et de filtrer des données depuis les fichiers JSON liés aux audits IFS NEO. Voici ce que vous pouvez faire :
        - Extraire des informations sur le site audité, les sous-traitances, produits exclus et bien plus.
        - Filtrer les données selon des UUID et chapitres spécifiques pour une extraction plus ciblée.
        - Modifier directement les données extraites avant de les télécharger sous forme de fichier Excel.
        
        **Fonctionnalités supplémentaires** :
        - Filtrage des données selon les UUID et chapitres
        - Possibilité de modifier les informations extraites
        - Téléchargement des données modifiées
        """)

    # Bouton pour naviguer vers la page NEO Extract
    if st.button("Aller à la version Extraction NEO"):
        st.write("Redirection vers la version **Extraction NEO**...")
        # Insérer le contenu de la page neoextract.py ici
        # Exemple : st.write(neoextract_page_function())

