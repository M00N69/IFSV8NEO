import streamlit as st
import json
import pandas as pd
from io import BytesIO
import requests

# Function to flatten the nested JSON structure
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

# Function to extract data from the flattened JSON
def extract_from_flattened(flattened_data, mapping, selected_fields):
    extracted_data = {}
    for label, flat_path in mapping.items():
        if label in selected_fields:
            extracted_data[label] = flattened_data.get(flat_path, 'N/A')
    return extracted_data

# Custom CSS for the table display
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

# Load the CSV mapping for UUIDs corresponding to NUM from a URL
def load_uuid_mapping_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        from io import StringIO
        csv_data = StringIO(response.text)
        uuid_mapping_df = pd.read_csv(csv_data)

        # Check if the columns 'UUID', 'Num', 'Chapitre', 'Theme', and 'SSTheme' exist and have non-empty values
        required_columns = ['UUID', 'Num', 'Chapitre', 'Theme', 'SSTheme']
        for column in required_columns:
            if column not in uuid_mapping_df.columns:
                st.error(f"Le fichier CSV doit contenir une colonne '{column}' avec des valeurs valides.")
                return {}

        uuid_mapping_df = uuid_mapping_df.dropna(subset=['UUID', 'Num'])  # Drop rows with empty 'UUID' or 'Num' values
        uuid_mapping_df['Chapitre'] = uuid_mapping_df['Chapitre'].astype(str).str.strip()
        uuid_mapping_df = uuid_mapping_df.drop_duplicates(subset=['Chapitre', 'Num'])  # Remove duplicate rows based on 'Chapitre' and 'Num'
        return uuid_mapping_df
    else:
        st.error("Impossible de charger le fichier CSV des UUID depuis l'URL fourni.")
        return pd.DataFrame()

# URL for the UUID CSV
UUID_MAPPING_URL = "https://raw.githubusercontent.com/M00N69/Gemini-Knowledge/refs/heads/main/IFSV8listUUID.csv"

UUID_MAPPING_DF = load_uuid_mapping_from_url(UUID_MAPPING_URL)

# Complete mapping based on your provided field names and JSON structure
FLATTENED_FIELD_MAPPING = {
    "Nom du site à auditer": "data_modules_food_8_questions_companyName_answer",
    "N° COID du portail": "data_modules_food_8_questions_companyCoid_answer",
    "Code GLN": "data_modules_food_8_questions_companyGln_answer_0_rootQuestions_companyGlnNumber_answer",
    "Rue": "data_modules_food_8_questions_companyStreetNo_answer",
    "Code postal": "data_modules_food_8_questions_companyZip_answer",
    "Nom de la ville": "data_modules_food_8_questions_companyCity_answer",
    "Pays": "data_modules_food_8_questions_companyCountry_answer",
    "Téléphone": "data_modules_food_8_questions_companyTelephone_answer",
    "Latitude": "data_modules_food_8_questions_companyGpsLatitude_answer",
    "Longitude": "data_modules_food_8_questions_companyGpsLongitude_answer",
    "Email": "data_modules_food_8_questions_companyEmail_answer",
    "Nom du siège social": "data_modules_food_8_questions_headquartersName_answer",
    "Rue (siège social)": "data_modules_food_8_questions_headquartersStreetNo_answer",
    "Nom de la ville (siège social)": "data_modules_food_8_questions_headquartersCity_answer",
    "Code postal (siège social)": "data_modules_food_8_questions_headquartersZip_answer",
    "Pays (siège social)": "data_modules_food_8_questions_headquartersCountry_answer",
    "Téléphone (siège social)": "data_modules_food_8_questions_headquartersTelephone_answer",
    "Code GLN": "data_modules_food_8_questions_companyGln_answer_0_rootQuestions_companyGlnNumber_answer",
    "Surface couverte de l'entreprise (m²)": "data_modules_food_8_questions_productionAreaSize_answer",
    "Nombre de bâtiments": "data_modules_food_8_questions_numberOfBuildings_answer",
    "Nombre de lignes de production": "data_modules_food_8_questions_numberOfProductionLines_answer",
    "Nombre d'étages": "data_modules_food_8_questions_numberOfFloors_answer",
    "Nombre maximum d'employés dans l'année, au pic de production": "data_modules_food_8_questions_numberOfEmployeesForTimeCalculation_answer",
    "Commentaires employés": "data_modules_food_8_questions_numberOfEmployeesDescription_answer",
    "Comment employees": "data_modules_food_8_questions_numberOfEmployeesDescription_en_answer",
    "Structures décentralisées": "data_modules_food_8_questions_companyStructureDecentralisedDescription_answer",
    "Fonctions centralisées": "data_modules_food_8_questions_companyStructureMultiLocationProductionDescription_answer",
    "Langue parlée et écrite sur le site": "data_modules_food_8_questions_workingLanguage_answer",
    "Langue du système qualité": "data_modules_food_8_questions_qmsLanguage_answer_0",
    "Audit scope EN": "data_modules_food_8_questions_scopeCertificateScopeDescription_en_answer",
    "Périmètre de l'audit FR": "data_modules_food_8_questions_scopeAuditScopeDescription_answer",
    "Process et activités": "data_modules_food_8_questions_scopeProductGroupsDescription_answer",
    "Activité saisonnière ? (O/N)": "data_modules_food_8_questions_seasonalProduction_answer",
    "Une partie du procédé de fabrication est-elle sous traitée? (OUI/NON)": "data_modules_food_8_questions_partlyOutsourcedProcesses_answer",
    "Si oui lister les procédés sous-traités": "data_modules_food_8_questions_partlyOutsourcedProcessesDescription_answer",
    "Avez-vous des produits totalement sous-traités? (OUI/NON)": "data_modules_food_8_questions_fullyOutsourcedProducts_answer",
    "Si oui, lister les produits totalement sous-traités": "data_modules_food_8_questions_fullyOutsourcedProductsDescription_answer",
    "Avez-vous des produits de négoce? (OUI/NON)": "data_modules_food_8_questions_tradedProductsBrokerActivity_answer",
    "Si oui, lister les produits de négoce": "data_modules_food_8_questions_tradedProductsBrokerActivityDescription_answer",
    "Produits à exclure du champ d'audit (OUI/NON)": "data_modules_food_8_questions_exclusions_answer",
    "Préciser les produits à exclure": "data_modules_food_8_questions_exclusionsDescription_answer"
}

# Streamlit app
st.title("IFS NEO Form Data Extractor")

# Step 1: Upload the JSON (.ifs) file
uploaded_json_file = st.file_uploader("Charger le fichier IFS de NEO", type="ifs")

if uploaded_json_file:
    try:
        # Step 2: Load the uploaded JSON file
        json_data = json.load(uploaded_json_file)

        # Step 3: Flatten the JSON data
        flattened_json_data_safe = flatten_json_safe(json_data)

        st.subheader("Exigences de la checklist pour Excel")
        if not UUID_MAPPING_DF.empty:
            # Filtering options with linked filtering
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

            # Extracting checklist requirements from flattened JSON data
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
                    "Response": response,
                    "Commentaire": ""
                })

            # Convert to DataFrame for Excel export
            df = pd.DataFrame(checklist_requirements)

            # Create the Excel file with column formatting
            output = BytesIO()

            # Create Excel writer and adjust column widths
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="Exigences de la checklist")

                # Access the worksheet to modify the formatting
                worksheet = writer.sheets["Exigences de la checklist"]

                # Adjust the width of each column based on the longest entry
                for col in worksheet.columns:
                    max_length = max(len(str(cell.value)) for cell in col)
                    col_letter = col[0].column_letter  # Get the column letter
                    worksheet.column_dimensions[col_letter].width = max_length + 5  # Adjust column width

            # Reset the position of the output to the start
            output.seek(0)

            # Provide the download button with the COID number in the filename
            st.download_button(
                label="Télécharger le fichier Excel",
                data=output,
                file_name='checklist_exigences.xlsx',
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("Impossible de charger les données des UUID. Veuillez vérifier l'URL.")

    except json.JSONDecodeError:
        st.error("Erreur lors du décodage du fichier JSON. Veuillez vous assurer qu'il est au format correct.")
else:
    st.write("Le fichier de NEO doit être un (.ifs)")
