# IFS NEO Form Data Extractor

Ce projet est une application Streamlit conçue pour extraire et manipuler des données à partir de fichiers JSON (.ifs) générés par le portail IFS NEO. L'application permet de flatter les structures JSON imbriquées, d'extraire des champs spécifiques, et de visualiser ou modifier les données extraites. Ce README fournit une vue d'ensemble détaillée de la structure du code, de la logique utilisée, des fonctions principales et des options disponibles.

## Structure du Code

Le code est organisé en plusieurs sections principales, chacune ayant une fonction spécifique :

### 1. Configuration de Streamlit

```python
import streamlit as st
st.set_page_config(layout="wide")
```

- **Description** : Cette section configure l'application Streamlit pour utiliser un layout large, offrant ainsi plus d'espace pour l'affichage des données.

### 2. Fonctions Utilitaires

#### a. Aplatissement des JSON

```python
def flatten_json_safe(nested_json, parent_key='', sep='_'):
    """Flatten a nested JSON dictionary, safely handling strings and primitives."""
    items = []
    if isinstance(nested_json, dict):
        for k, v in nested_json.items():
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_json_safe(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    items.extend(flatten_json_safe(item, f'{new_key}{sep}{i}', sep=sep).items())
            else:
                items.append((new_key, v))
    else:
        items.append((parent_key, nested_json))
    return dict(items)
```

- **Description** : Cette fonction aplatit une structure JSON imbriquée en gérant les chaînes de caractères et les primitives de manière sécurisée. Elle transforme une structure JSON complexe en une structure plate, facilitant ainsi l'extraction des données.

#### b. Extraction des Données

```python
def extract_from_flattened(flattened_data, mapping, selected_fields):
    extracted_data = {}
    for label, flat_path in mapping.items():
        if label in selected_fields:
            extracted_data[label] = flattened_data.get(flat_path, 'N/A')
    return extracted_data
```

- **Description** : Cette fonction extrait des données spécifiques à partir des données JSON aplaties en utilisant un mappage et une liste de champs sélectionnés. Elle permet de récupérer uniquement les champs nécessaires pour l'analyse ou la visualisation.

#### c. Application du CSS pour les Tables

```python
def apply_table_css():
    st.markdown(
        """
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: #f9f9f9;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        </style>
        """, unsafe_allow_html=True
    )
```

- **Description** : Cette fonction applique un style CSS personnalisé pour l'affichage des tables, améliorant ainsi la lisibilité et l'esthétique des données affichées.

#### d. Chargement du Mappage des UUID

```python
def load_uuid_mapping_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        from io import StringIO
        csv_data = StringIO(response.text)
        uuid_mapping_df = pd.read_csv(csv_data)

        required_columns = ['UUID', 'Num', 'Chapitre', 'Theme', 'SSTheme']
        for column in required_columns:
            if column not in uuid_mapping_df.columns:
                st.error(f"Le fichier CSV doit contenir une colonne '{column}' avec des valeurs valides.")
                return {}

        uuid_mapping_df = uuid_mapping_df.dropna(subset=['UUID', 'Num'])
        uuid_mapping_df['Chapitre'] = uuid_mapping_df['Chapitre'].astype(str).str.strip()
        uuid_mapping_df = uuid_mapping_df.drop_duplicates(subset=['Chapitre', 'Num'])
        return uuid_mapping_df
    else:
        st.error("Impossible de charger le fichier CSV des UUID depuis l'URL fourni.")
        return pd.DataFrame()
```

- **Description** : Cette fonction charge un fichier CSV de mappage des UUID depuis une URL et vérifie la présence des colonnes requises. Elle nettoie également les données en supprimant les lignes dupliquées et les valeurs manquantes.

### 3. Variables Globales

```python
UUID_MAPPING_URL = "https://raw.githubusercontent.com/M00N69/Gemini-Knowledge/refs/heads/main/IFSV8listUUID.csv"
UUID_MAPPING_DF = load_uuid_mapping_from_url(UUID_MAPPING_URL)

FLATTENED_FIELD_MAPPING = {
    "Nom du site à auditer": "data_modules_food_8_questions_companyName_answer",
    "N° COID du portail": "data_modules_food_8_questions_companyCoid_answer",
    # ... autres mappages ...
}
```

- **Description** : Ces variables globales contiennent l'URL du fichier CSV de mappage des UUID, le DataFrame résultant du chargement de ce fichier, et un dictionnaire de mappage des champs JSON aplatis vers des labels lisibles.

### 4. Interface Utilisateur Streamlit

#### a. Menu de Navigation

```python
st.sidebar.title("Menu de Navigation")
option = st.sidebar.radio("Choisissez une option:", ["Extraction des données", "Exigences de la checklist", "Modification des données EN PROJET", "Exportation EN PROJET", "Plan d'actions EN PROJET"])
```

- **Description** : Cette section crée un menu de navigation dans la barre latérale de Streamlit, permettant à l'utilisateur de choisir parmi plusieurs options.

#### b. Chargement du Fichier JSON

```python
st.title("IFS NEO Form Data Extractor")
uploaded_json_file = st.file_uploader("Charger le fichier IFS de NEO", type="ifs")
```

- **Description** : Cette section permet à l'utilisateur de télécharger un fichier JSON (.ifs) via l'interface Streamlit.

#### c. Extraction des Données

```python
if uploaded_json_file:
    try:
        json_data = json.load(uploaded_json_file)
        flattened_json_data_safe = flatten_json_safe(json_data)

        if option == "Extraction des données":
            st.subheader("Champs disponibles pour l'extraction")
            select_all = st.checkbox("Sélectionner tous les champs")
            if select_all:
                selected_fields = list(FLATTENED_FIELD_MAPPING.keys())
            else:
                selected_fields = st.multiselect("Sélectionnez les champs que vous souhaitez extraire", list(FLATTENED_FIELD_MAPPING.keys()))
            if selected_fields:
                extracted_data = extract_from_flattened(flattened_json_data_safe, FLATTENED_FIELD_MAPPING, selected_fields)
                st.subheader("Données extraites")
                edit_mode = st.checkbox("Modifier les données")
                updated_data = extracted_data.copy()

                if edit_mode:
                    for field, value in extracted_data.items():
                        if field in ["Périmètre de l'audit", "Process et activités", "Si oui lister les procédés sous-traités", "Si oui, lister les produits totalement sous-traités", "Si oui, lister les produits de négoce", "Préciser les produits à exclure"]:
                            updated_data[field] = st.text_area(f"{field}", value=value, height=150)
                        else:
                            updated_data[field] = st.text_input(f"{field}", value=value)
                else:
                    apply_table_css()
                    table_html = "<table><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>"
                    for field, value in extracted_data.items():
                        table_html += f"<tr><td>{field}</td><td>{value}</td></tr>"
                    table_html += "</tbody></table>"
                    st.markdown(table_html, unsafe_allow_html=True)

                df = pd.DataFrame(list(updated_data.items()), columns=["Field", "Value"])
                numero_coid = updated_data.get("N° COID du portail", "inconnu")
                output = BytesIO()

                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name="Données extraites")
                    worksheet = writer.sheets["Données extraites"]
                    for col in worksheet.columns:
                        max_length = max(len(str(cell.value)) for cell in col)
                        col_letter = col[0].column_letter
                        worksheet.column_dimensions[col_letter].width = max_length + 5

                output.seek(0)
                st.download_button(
                    label="Télécharger le fichier Excel",
                    data=output,
                    file_name=f'extraction_{numero_coid}.xlsx',
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    except json.JSONDecodeError:
        st.error("Erreur lors du décodage du fichier JSON. Veuillez vous assurer qu'il est au format correct.")
else:
    st.write("Le fichier de NEO doit être un (.ifs)")
```

- **Description** : Cette section gère le chargement du fichier JSON, l'aplatissement des données JSON, et l'extraction des champs sélectionnés par l'utilisateur. Les données extraites peuvent être affichées en lecture seule ou modifiées via des widgets Streamlit. L'utilisateur peut également télécharger les données extraites sous forme de fichier Excel avec un formatage personnalisé.

#### d. Exigences de la Checklist

```python
elif option == "Exigences de la checklist":
    st.subheader("Exigences de la checklist")
    if not UUID_MAPPING_DF.empty:
        chapitre_options = ["Tous"] + sorted(UUID_MAPPING_DF['Chapitre'].dropna().unique())
        chapitre_filter = st.selectbox("Filtrer par Chapitre", options=chapitre_options)
        filtered_df = UUID_MAPPING_DF

        if chapitre_filter != "Tous":
            filtered_df = filtered_df[filtered_df['Chapitre'] == chapitre_filter]
            theme_options = ["Tous"] + sorted(filtered_df['Theme'].dropna().unique())
        else:
            theme_options = ["Tous"] + sorted(UUID_MAPPING_DF['Theme'].dropna().unique())
        theme_filter = st.selectbox("Filtrer par Thème", options=theme_options)

        if theme_filter != "Tous":
            filtered_df = filtered_df[filtered_df['Theme'] == theme_filter]
            sstheme_options = ["Tous"] + sorted(filtered_df['SSTheme'].dropna().unique())
        else:
            sstheme_options = ["Tous"] + sorted(UUID_MAPPING_DF['SSTheme'].dropna().unique())
        sstheme_filter = st.selectbox("Filtrer par Sous-Thème", options=sstheme_options)

        if sstheme_filter != "Tous":
            filtered_df = filtered_df[filtered_df['SSTheme'] == sstheme_filter]

        checklist_requirements = []
        for _, row in filtered_df.iterrows():
            key = row['Num']
            uuid = row['UUID']
            prefix = f"data_modules_food_8_checklists_checklistFood8_resultScorings_{uuid}"
            explanation_text = flattened_json_data_safe.get(f"{prefix}_answers_englishExplanationText", "N/A")
            detailed_explanation = flattened_json_data_safe.get(f"{prefix}_answers_explanationText", "N/A")
            score_label = flattened_json_data_safe.get(f"{prefix}_score_label", "N/A")
            response = flattened_json_data_safe.get(f"{prefix}_answers_fieldAnswers", "N/A")
            checklist_requirements.append({
                "Num": key,
                "Explanation": explanation_text,
                "Detailed Explanation": detailed_explanation,
                "Score": score_label,
                "Response": response
            })

        apply_table_css()
        table_html = "<table><thead><tr><th>Numéro d'exigence</th><th>Explication</th><th>Explication Détaillée</th><th>Note</th><th>Réponse</th></tr></thead><tbody>"
        for req in checklist_requirements:
            table_html += f"<tr><td>{req['Num']}</td><td>{req['Explanation']}</td><td>{req['Detailed Explanation']}</td><td>{req['Score']}</td><td>{req['Response']}</td></tr>"
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.error("Impossible de charger les données des UUID. Veuillez vérifier l'URL.")
```

- **Description** : Cette section permet à l'utilisateur de filtrer les exigences de la checklist par Chapitre, Thème, et Sous-Thème. Les exigences correspondantes sont extraites des données JSON aplaties et affichées dans une table.

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
