import json
import pandas as pd
import streamlit as st
from io import BytesIO

# Function to extract nested data safely
def extract_nested_data(data, keys):
    """Recursively extract data from a nested dictionary"""
    if isinstance(data, dict):
        return data.get(keys[0], 'N/A') if len(keys) == 1 else extract_nested_data(data.get(keys[0], {}), keys[1:])
    return 'N/A'

# Full field mapping based on the provided structure
FIELD_MAPPING = {
    # 1. Information sur l'entreprise
    "Nom du site à auditer": ["companyInfo", "companyName"],
    "N° COID du portail": ["companyInfo", "companyCoid"],
    "Code GLN": ["companyInfo", "companyGlnNumber"],
    "Rue": ["companyInfo", "companyStreetNo"],
    "Code postal": ["companyInfo", "companyZip"],
    "Nom de la ville": ["companyInfo", "companyCity"],
    "Pays": ["companyInfo", "companyCountry"],
    "Téléphone": ["companyInfo", "companyTelephone"],
    "Latitude": ["companyInfo", "companyGpsLatitude"],
    "Longitude": ["companyInfo", "companyGpsLongitude"],
    "Email": ["companyInfo", "companyEmail"],

    # 2. Organisation de l'entreprise et de l'audit
    "Nom du siège social": ["headquarters", "headquartersName"],
    "Rue (siège social)": ["headquarters", "headquartersStreetNo"],
    "Nom de la ville (siège social)": ["headquarters", "headquartersCity"],
    "Code postal (siège social)": ["headquarters", "headquartersZip"],
    "Pays (siège social)": ["headquarters", "headquartersCountry"],
    "Téléphone (siège social)": ["headquarters", "headquartersTelephone"],
    
    # 3. Organisation du site
    "Surface couverte de l'entreprise (m²)": ["siteInfo", "productionAreaSize"],
    "Nombre de bâtiments": ["siteInfo", "numberOfBuildings"],
    "Nombre de lignes de production": ["siteInfo", "numberOfProductionLines"],
    "Nombre d'étages": ["siteInfo", "numberOfFloors"],
    "Nombre maximum d'employés dans l'année, au pic de production": ["siteInfo", "numberOfEmployeesForTimeCalculation"],
    "Langue parlée et écrite sur le site": ["siteInfo", "workingLanguage"],
    
    # 4. Produits concernés et champ de l'audit
    "Norme souhaitée": ["auditInfo", "previousCertificationStandardVersion"],
    "Périmètre de l'audit": ["auditInfo", "scopeCertificateScopeDescription"],
    "Process et activités": ["auditInfo", "scopeProductGroupsDescription"],
    "Activité saisonnière ? (O/N)": ["auditInfo", "seasonalProduction"],

    # Outsourcing and Products
    "Une partie du procédé de fabrication est-elle sous traitée? (OUI/NON)": ["outsourcingInfo", "partlyOutsourcedProcesses"],
    "Si oui, lister les procédés sous-traités": ["outsourcingInfo", "partlyOutsourcedProcessesDescription"],
    "Avez-vous des produits totalement sous-traités? (OUI/NON)": ["outsourcingInfo", "fullyOutsourcedProducts"],
    "Si oui, lister les produits totalement sous-traités": ["outsourcingInfo", "fullyOutsourcedProductsDescription"],
    "Avez-vous des produits de négoce? (OUI/NON)": ["outsourcingInfo", "tradedProductsBrokerActivity"],
    "Si oui, lister les produits de négoce": ["outsourcingInfo", "tradedProductsBrokerActivityDescription"],
    "Produits à exclure du champ d'audit (OUI/NON)": ["outsourcingInfo", "exclusions"],
    "Préciser les produits à exclure": ["outsourcingInfo", "exclusionsDescription"]
}

# Custom CSS for the DataFrame display
def apply_table_css():
    st.markdown(
        """
        <style>
        .dataframe th, .dataframe td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .dataframe {
            border: 1px solid #ddd;
            border-collapse: collapse;
            width: 100%;
            background-color: #f9f9f9;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Step 1: Upload the JSON (.ifs) file
uploaded_json_file = st.file_uploader("Upload JSON (IFS) file", type="ifs")

if uploaded_json_file:
    try:
        # Step 2: Load the uploaded JSON file
        json_data = json.load(uploaded_json_file)

        # Show part of the JSON structure for debugging
        st.subheader("Preview of Uploaded JSON Data")
        st.json(json_data)  # Displaying the JSON structure to help debug

        # Step 3: Extract data from JSON based on the predefined mapping
        extracted_data = {}

        for label, path in FIELD_MAPPING.items():
            extracted_data[label] = extract_nested_data(json_data, path)

        # Step 4: Create a DataFrame from the extracted data
        extracted_df = pd.DataFrame(list(extracted_data.items()), columns=["Field", "Value"])

        # Step 5: Display the DataFrame in Streamlit with CSS
        apply_table_css()  # Apply custom table CSS
        st.title("Extracted Data from JSON (IFS)")
        st.write(extracted_df)

        # Step 6: Function to convert DataFrame to Excel format in memory
        def convert_df_to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return output.getvalue()

        # Convert DataFrame to Excel for download
        excel_data = convert_df_to_excel(extracted_df)

        # Step 7: Provide option to download the extracted data as Excel
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




