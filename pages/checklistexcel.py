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
                checklist_requirements.append({
                    "Num": key,
                    "Explanation": explanation_text,
                    "Detailed Explanation": detailed_explanation,
                    "Score": score_label,
                    "Commentaire": ""
                })

            # Convert to DataFrame for Excel export
            df = pd.DataFrame(checklist_requirements)

            # Ensure the 'Num' column is of type string
            df['Num'] = df['Num'].astype(str)

            # Create the Excel file with column formatting
            output = BytesIO()

            # Create Excel writer and adjust column widths
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Write the main sheet
                df.to_excel(writer, index=False, sheet_name="Exigences de la checklist")

                # Access the worksheet to modify the formatting
                worksheet = writer.sheets["Exigences de la checklist"]
                worksheet.column_dimensions['B'].width = 50
                worksheet.column_dimensions['C'].width = 50
                worksheet.column_dimensions['F'].width = 50

                for col in ['B', 'C', 'F']:
                    for cell in worksheet[col]:
                        cell.alignment = cell.alignment.copy(wrapText=True)

                # Filter and write the "CO" sheet
                df_co = df[df['Num'].str.contains(r'\*', na=False, regex=True)]
                df_co.to_excel(writer, index=False, sheet_name="CO")
                worksheet_co = writer.sheets["CO"]
                worksheet_co.column_dimensions['B'].width = 50
                worksheet_co.column_dimensions['C'].width = 50
                worksheet_co.column_dimensions['F'].width = 50

                for col in ['B', 'C', 'F']:
                    for cell in worksheet_co[col]:
                        cell.alignment = cell.alignment.copy(wrapText=True)

                # Filter and write the "NA" sheet
                df_na = df[df['Score'] == "NA"]
                df_na.to_excel(writer, index=False, sheet_name="NA")
                worksheet_na = writer.sheets["NA"]
                worksheet_na.column_dimensions['B'].width = 50
                worksheet_na.column_dimensions['C'].width = 50
                worksheet_na.column_dimensions['F'].width = 50

                for col in ['B', 'C', 'F']:
                    for cell in worksheet_na[col]:
                        cell.alignment = cell.alignment.copy(wrapText=True)

                # Filter and write the "Plan d'action" sheet
                df_plan_action = df[(df['Score'] != "A") & (df['Score'] != "NA")]
                df_plan_action.to_excel(writer, index=False, sheet_name="Plan d'action")
                worksheet_plan_action = writer.sheets["Plan d'action"]
                worksheet_plan_action.column_dimensions['B'].width = 50
                worksheet_plan_action.column_dimensions['C'].width = 50
                worksheet_plan_action.column_dimensions['F'].width = 50

                for col in ['B', 'C', 'F']:
                    for cell in worksheet_plan_action[col]:
                        cell.alignment = cell.alignment.copy(wrapText=True)

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
