import json
import pandas as pd
import streamlit as st

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

# Step 2: Upload the JSON (.ifs) file
uploaded_json_file = st.file_uploader("Upload JSON (IFS) file", type="ifs")

if uploaded_json_file:
    try:
        # Step 3: Load the uploaded JSON file
        json_data = json.load(uploaded_json_file)
        
        # Step 4: Extract data from JSON based on the predefined mapping
        extracted_data = {}
        
        for label, json_key in FIELD_MAPPING.items():
            if json_key:
                # Safely access the nested JSON structure
                extracted_data[label] = json_data.get('questions', {}).get(json_key, {}).get('answer', 'N/A')
            else:
                extracted_data[label] = 'N/A'  # No mapping available

        # Step 5: Create a DataFrame from the extracted data
        extracted_df = pd.DataFrame(list(extracted_data.items()), columns=["Field", "Value"])
        
        # Step 6: Display the DataFrame in Streamlit
        st.title("Extracted Data from JSON (IFS)")
        st.write(extracted_df)

        # Step 7: Provide option to download the extracted data as Excel
        def convert_df_to_excel(df):
            return df.to_excel(index=False, engine='xlsxwriter')

        # Convert to Excel
        excel_data = convert_df_to_excel(extracted_df)
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
