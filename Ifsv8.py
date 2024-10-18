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

# Step 2: Upload the JSON (.ifs) file
uploaded_json_file = st.file_uploader("Upload JSON (IFS) file", type="ifs")

if uploaded_json_file:
    try:
        # Step 3: Load the uploaded JSON file and print part of the structure for inspection
        json_data = json.load(uploaded_json_file)
        
        # Step 4: Display first 1000 characters of the JSON data for inspection
        st.subheader("Preview of Uploaded JSON (IFS) Data")
        st.text(json.dumps(json_data, indent=2)[:1000])  # Show first 1000 characters for inspection

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

        # Step 7: Display the DataFrame in Streamlit
        st.title("Extracted Data from JSON (IFS)")
        st.write(extracted_df)

    except json.JSONDecodeError:
        st.error("Error decoding the JSON file. Please ensure it is in the correct format.")
else:
    st.write("Please upload a JSON file in .ifs format to proceed.")


