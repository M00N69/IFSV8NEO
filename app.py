import streamlit as st

# Configuration de la page en mode large
st.set_page_config(layout="wide")

# Titre principal
st.title("Extracteur de données du formulaire IFS NEO")

# Explication pour utiliser le menu en haut à gauche
st.markdown("""
### Instructions :
Pour accéder aux différentes sections du projet, utilisez les **pages** situées dans le **menu en haut à gauche**. 
Vous pouvez naviguer entre :
- **Rapport IFS V8** : Pour extraire les données des fichiers liés aux audits IFS V8.
- **Extraction NEO** : Pour utiliser la version avancée avec des options de filtrage et modification de données.

Cliquez sur les pages dans la barre latérale pour accéder à ces différentes versions.
""")

# Explication générale dans un expander
with st.expander("Explication des fonctionnalités générales du projet"):
    st.write("""
    Ce projet est conçu pour extraire des informations depuis des fichiers JSON (.ifs) issus des audits IFS.
    Ces fichiers peuvent contenir des structures de données complexes qui nécessitent un "aplatissement" (flattening) pour extraire les données utiles.
    
    ### Fonctionnalités des deux versions :
    - **Rapport IFS V8** : Extraction des informations des fichiers liés à un audit IFS V8.
    - **Extraction NEO** : Une version plus avancée qui permet de filtrer et modifier les données extraites, avec des options supplémentaires basées sur des UUID spécifiques.
    
    Utilisez les pages du **menu en haut à gauche** pour explorer ces versions.
    """)

# Explications détaillées pour chaque version
with st.expander("Détails de la version Rapport IFS V8"):
    st.write("""
    ### Rapport IFS V8 :
    Cette version permet d'extraire des informations spécifiques d'un fichier JSON lié à un audit IFS V8. Vous pouvez utiliser cette version pour obtenir des informations telles que :
    
    - Nom du site, Code GLN, Adresse, Ville, Pays, etc.
    - Coordonnées GPS (Latitude, Longitude)
    - Informations sur le siège social et la production
    - Sous-traitance et exclusions du champ d'audit

    #### Fonctionnalités :
    - Chargement d'un fichier JSON IFS V8
    - Extraction des données et affichage sous forme de tableau
    - Téléchargement des données au format Excel
    """)

with st.expander("Détails de la version Extraction NEO"):
    st.write("""
    ### Extraction NEO :
    Cette version avancée permet d'extraire, filtrer, et modifier les données depuis les fichiers JSON d'audits IFS NEO. Elle est particulièrement utile pour des analyses plus complexes.
    
    #### Fonctionnalités supplémentaires :
    - Filtrage des données selon des UUID et chapitres spécifiques
    - Possibilité de modifier les informations extraites avant de les télécharger sous forme de fichier Excel
    - Analyse détaillée des exigences des audits
    
    Utilisez les **pages dans le menu à gauche** pour explorer cette version.
    """)

# Ajout d'un message pour expliquer la navigation
st.info("Utilisez le **menu des pages en haut à gauche** pour accéder aux différentes sections du projet.")


