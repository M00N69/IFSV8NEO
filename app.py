import streamlit as st

# Configuration de la page en mode large
st.set_page_config(layout="wide")

# Titre principal
st.title("Extracteur de données du formulaire IFS NEO")

# Menu latéral pour naviguer entre les versions du projet
st.sidebar.title("Menu de navigation")
version_projet = st.sidebar.radio(
    "Sélectionnez la version du projet à explorer :",
    ('Rapport IFS V8', 'Extraction NEO')
)

# Explication générale dans un expander
with st.expander("Explication des fonctionnalités générales du projet"):
    st.write("""
    Ce projet est conçu pour extraire des informations depuis des fichiers JSON (.ifs) issus des audits IFS.
    Ces fichiers peuvent contenir des structures de données complexes qui nécessitent un "aplatissement" (flattening) pour extraire les données utiles.
    
    Les deux versions disponibles de l'outil sont :
    - **Rapport IFS V8** : Extraction des informations des fichiers liés à un audit IFS V8.
    - **Extraction NEO** : Une version plus avancée qui permet également de filtrer et modifier les données extraites, avec des options supplémentaires basées sur des UUID spécifiques.
    
    Utilisez le **menu latéral** pour sélectionner la version du projet que vous souhaitez explorer.
    """)

# Explications détaillées pour chaque version en fonction de la sélection dans le menu latéral
if version_projet == 'Rapport IFS V8':
    # Expander explicatif pour IFS V8
    with st.expander("Détails de la version Rapport IFS V8"):
        st.write("""
        ### Rapport IFS V8 :
        Cette version permet d'extraire des informations spécifiques d'un fichier JSON lié à un audit IFS V8. Vous pouvez utiliser cette version pour obtenir des informations telles que :
        
        - **Nom du site à auditer** : Le nom de l'entreprise ou du site audité.
        - **N° COID du portail** : Le numéro COID de l'entreprise.
        - **Code GLN** : Le code GLN de l'entreprise (avec options pour plusieurs codes).
        - **Adresse** : Rue, Code postal, Ville, Pays.
        - **Coordonnées GPS** : Latitude et Longitude du site.
        - **Email et Téléphone** : Informations de contact.
        - **Informations sur le siège social** : Nom, Rue, Ville, Code postal, Pays.
        - **Données sur la production** : Surface couverte de l'entreprise, nombre de bâtiments, lignes de production, nombre d'employés au pic de production.
        - **Langue de travail** : Langue parlée sur le site.
        - **Sous-traitance et négoce** : Informations sur les processus sous-traités, produits totalement sous-traités ou de négoce.
        - **Produits exclus de l'audit** : Liste des produits ou processus exclus du champ d'audit.
        
        #### Fonctionnalités :
        - **Chargement d'un fichier JSON** : Vous pouvez télécharger un fichier au format .ifs qui contient les données de l'audit IFS V8.
        - **Extraction des données spécifiques** : Les données sont extraites et affichées sous forme de tableau.
        - **Téléchargement des données au format Excel** : Une fois les données extraites, vous avez la possibilité de les télécharger sous forme de fichier Excel.
        
        ### Mode d'emploi :
        - Utilisez le **menu latéral** pour charger un fichier JSON et voir les données extraites.
        - Une fois le fichier chargé, les informations extraites s'afficheront directement sous forme de tableau.
        """)

elif version_projet == 'Extraction NEO':
    # Expander explicatif pour Extraction NEO
    with st.expander("Détails de la version Extraction NEO"):
        st.write("""
        ### Extraction NEO :
        Cette version avancée permet d'extraire, filtrer, et modifier les données depuis les fichiers JSON d'audits IFS NEO. Elle est particulièrement utile pour des analyses plus complexes avec des besoins spécifiques d'extraction de données, basés sur des UUID et des chapitres spécifiques.
        
        #### Données extraites :
        - **Nom du site** : Le nom de l'entreprise ou du site audité.
        - **Sous-traitance et négoce** : Identifiez et listez les produits et processus sous-traités.
        - **Exclusions** : Déterminez quels produits ou processus sont exclus du champ d'audit.
        
        #### Fonctionnalités supplémentaires :
        - **Filtrage des données** : Vous pouvez filtrer les données extraites en fonction de chapitres ou de UUID spécifiques, ce qui permet une extraction plus précise.
        - **Modification des données** : Vous pouvez modifier directement les informations extraites avant de les télécharger.
        - **Téléchargement des données modifiées** : Les données modifiées peuvent être téléchargées sous forme de fichier Excel pour une utilisation ultérieure.
        
        ### Mode d'emploi :
        - Utilisez le **menu latéral** pour charger un fichier JSON et appliquer des filtres spécifiques selon les chapitres ou les UUID.
        - Les données filtrées s'afficheront sous forme de tableau et pourront être modifiées directement dans l'application.
        - Vous pouvez ensuite télécharger le fichier modifié sous forme de fichier Excel.
        """)

# Rendu conditionnel des pages en fonction de la version choisie
if version_projet == 'Rapport IFS V8':
    st.header("Page Rapport IFS V8")
    st.write("Vous avez sélectionné la version **Rapport IFS V8**.")
    # Ici, tu incluras le code spécifique à la version Rapport IFS V8 (importer depuis ifsv8.py)
    # Par exemple : ifsv8_page_function()

elif version_projet == 'Extraction NEO':
    st.header("Page Extraction NEO")
    st.write("Vous avez sélectionné la version **Extraction NEO**.")
    # Ici, tu incluras le code spécifique à la version Extraction NEO (importer depuis neoextract.py)
    # Par exemple : neoextract_page_function()

