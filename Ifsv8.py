import json
import pandas as pd
import streamlit as st
from io import BytesIO

# Step 1: Hardcoded JSON field mapping based on your updated information
FIELD_MAPPING = {
    "Nom du site à auditer": "companyName",
    "Statut légal": "",  # No mapping available
    "Site internet": "",  # No mapping available
    "N° SIRET": "",  # No mapping available
    "N° COID du portail (si applicable)": "companyCoid",
    "Code GLN": "companyGlnNumber",
    "Rue": "companyStreetNo",
    "Code postal": "companyZip",
    "Nom de la ville": "companyCity",
    "Pays": "companyCountry",
    "Téléphone": "companyTelephone",
    "Coordonnées GPS du site à évaluer (Latitude)": "companyGpsLatitude",
    "Coordonnées GPS du site à évaluer (Longitude)": "companyGpsLongitude",
    "Email": "companyEmail",
    "Nom du siège social": "headquartersName",
    "Rue (siège social)": "headquartersStreetNo",
    "Nom de la ville (siège social)": "headquartersCity",
    "Code postal (siège social)": "headquartersZip",
    "Pays (siège social)": "headquartersCountry",
    "Téléphone (siège social)": "headquartersTelephone",
    "Surface couverte de l'entreprise (m²) - Totale": "productionAreaSize",
    "Nombre de batiments": "numberOfBuildings",
    "Nombre de ligne": "numberOfProductionLines",
    "Nombre d'étages": "numberOfFloors",
    "Nombre maximum d'employés dans l'année, au pic de production": "numberOfEmployeesForTimeCalculation",
    "Langue parlée et écrite sur le site": "workingLanguage",
    "Norme souhaitée": "previousCertificationStandardVersion",
    "Périmètre de l'audit": "scopeCertificateScopeDescription",
    "Process et activités": "scopeProductGroupsDescription",
    "Activité saisonnière ? (O/N)": "seasonalProduction",
    "Une partie du procédé de fabrication est-elle sous traitée? (OUI/NON)": "partlyOutsourcedProcesses",
    "Si oui, lister les procédés sous-traités": "partlyOutsourcedProcessesDescription",
    "Avez-vous des produits totalement sous-traités? (OUI/NON)": "fullyOutsourcedProducts",
    "Si oui, lister les produits totalement sous-traités": "fullyOutsourcedProductsDescription",
    "Avez-vous des produits de négoce? (OUI/NON)": "tradedProductsBrokerActivity",
    "Si oui, lister les produits de négoce": "tradedProductsBrokerActivityDescription",
    "Produits à exclure du champ d'audit (OUI/NON)": "exclusions",
    "Préciser les produits à exclure": "exclusionsDescription"
}

# Step 2: Function to add custom CSS for DataFrame styling
def local_css():
    st.markdown(
        """
        <style>
        .dataframe {
            border: 1px solid #ddd;
            border-collapse: collapse;
            width: 100%;
        }
        .dataframe td, .dataframe th {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .dataframe th {
            background-color: #f2f2f2;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Step 3: Upload the JSON (.ifs) file
uploaded_json_file = st.file_uploader("Upload JSON (IFS) file", type="ifs")

if uploaded_json_file:
    try:
        # Step 4: Load the uploaded JSON file
        json_data = json.load(uploaded_json_file)
        
        # Step 5: Extract data from JSON based on the predefined mapping
        extracted_data = {}
        
        for label, json_key in FIELD_MAPPING.items():
            if json_key:
                # Safely access the nested JSON structure
                extracted_data[label] = json_data.get('questions', {}).get(json_key, {}).get('answer', 'N/A')
            else:
                extracted_data[label] = 'N/A'  # No mapping available

        # Filter out any fields with 'N/A'
        extracted_data = {k: v for k, v in extracted_data.items() if v != 'N/A'}

        # Step 6: Create a DataFrame from the extracted data
        extracted_df = pd.DataFrame(list(extracted_data.items()), columns=["Field", "Value"])

        # Step 7: Apply CSS styling to the DataFrame
        local_css()
        st.title("Extracted Data from JSON (IFS)")
        st.write(extracted_df.to_html(index=False), unsafe_allow_html=True)

        # Step 8: Function to convert DataFrame to Excel format in memory
        def convert_df_to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            processed_data = output.getvalue()
            return processed_data

        # Convert DataFrame to Excel for download
        excel_data = convert_df_to_excel(extracted_df)
        
        # Step 9: Provide option to download the extracted data as Excel
        st.download_button(
            label="Download as Excel",
            data=excel_data,
            file_name="extracted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except json.JSONDecodeError:
        st.error("Error decoding the JSON file. Please ensure it is in the correct format.")
else:
    st.write("Please upload a JSON file in .ifs format to proceed.")


