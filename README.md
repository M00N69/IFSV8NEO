# IFS NEO Form Data Extractor

Ce projet est une application Streamlit conçue pour extraire et manipuler des données à partir de fichiers JSON (.ifs) générés par le portail IFS NEO. L'application permet de flatter les structures JSON imbriquées, d'extraire des champs spécifiques, et de visualiser ou modifier les données extraites.

## Structure du Code

Le code est organisé en plusieurs fonctions principales et sections :

1. **Configuration de Streamlit** :
   - `st.set_page_config(layout="wide")` : Configure l'application Streamlit en mode large.

2. **Fonctions Utilitaires** :
   - `flatten_json_safe(nested_json, parent_key='', sep='_')` : Aplatit une structure JSON imbriquée en gérant les chaînes de caractères et les primitives de manière sécurisée.
   - `extract_from_flattened(flattened_data, mapping, selected_fields)` : Extrait des données spécifiques à partir des données JSON aplaties en utilisant un mappage et une liste de champs sélectionnés.
   - `apply_table_css()` : Applique un style CSS personnalisé pour l'affichage des tables.
   - `load_uuid_mapping_from_url(url)` : Charge un fichier CSV de mappage des UUID depuis une URL et vérifie la présence des colonnes requises.

3. **Variables Globales** :
   - `UUID_MAPPING_URL` : URL du fichier CSV de mappage des UUID.
   - `UUID_MAPPING_DF` : DataFrame contenant les données de mappage des UUID chargées depuis l'URL.
   - `FLATTENED_FIELD_MAPPING` : Dictionnaire de mappage des champs JSON aplatis vers des labels lisibles.

4. **Interface Utilisateur Streamlit** :
   - **Menu de Navigation** : Permet à l'utilisateur de choisir parmi plusieurs options (Extraction des données, Exigences de la checklist, etc.).
   - **Chargement du Fichier JSON** : Permet à l'utilisateur de télécharger un fichier JSON (.ifs).
   - **Extraction des Données** : Affiche les champs disponibles pour l'extraction et permet à l'utilisateur de sélectionner les champs à extraire. Les données extraites peuvent être affichées en lecture seule ou modifiées.
   - **Exigences de la Checklist** : Affiche les exigences de la checklist en fonction des filtres sélectionnés (Chapitre, Thème, Sous-Thème).
   - **Téléchargement des Données** : Permet à l'utilisateur de télécharger les données extraites sous forme de fichier Excel avec un formatage personnalisé.

## Fonctionnement

1. **Chargement du Fichier JSON** :
   - L'utilisateur télécharge un fichier JSON (.ifs) via l'interface Streamlit.
   - Le fichier est chargé et la structure JSON est aplatie pour faciliter l'extraction des données.

2. **Extraction des Données** :
   - L'utilisateur sélectionne les champs à extraire parmi une liste de champs disponibles.
   - Les données correspondantes sont extraites et affichées dans une table ou peuvent être modifiées via des widgets Streamlit.

3. **Exigences de la Checklist** :
   - L'utilisateur peut filtrer les exigences de la checklist par Chapitre, Thème, et Sous-Thème.
   - Les exigences correspondantes sont extraites des données JSON aplaties et affichées dans une table.

4. **Téléchargement des Données** :
   - Les données extraites peuvent être téléchargées sous forme de fichier Excel avec un formatage personnalisé. Le nom du fichier inclut le numéro COID pour une identification facile.

## Options

- **Extraction des données** : Permet de sélectionner et d'extraire des champs spécifiques à partir du fichier JSON.
- **Exigences de la checklist** : Affiche les exigences de la checklist en fonction des filtres sélectionnés.
- **Modification des données EN PROJET** : Fonctionnalité en cours de développement pour modifier les données extraites.
- **Exportation EN PROJET** : Fonctionnalité en cours de développement pour exporter les données modifiées.
- **Plan d'actions EN PROJET** : Fonctionnalité en cours de développement pour gérer les plans d'actions.

## Conclusion

Ce projet offre une solution complète pour extraire, visualiser, et manipuler des données à partir de fichiers JSON générés par le portail IFS NEO. Les fonctionnalités actuelles permettent une extraction et une visualisation efficaces des données, avec des options de filtrage et de téléchargement pour une utilisation pratique. Des fonctionnalités supplémentaires sont en cours de développement pour offrir une expérience utilisateur encore plus riche.
