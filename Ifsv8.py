import json
import streamlit as st

# Function to extract nested data safely, handling lists when necessary
def extract_nested_data(data, keys):
    """Recursively extract data from a nested dictionary, handling lists."""
    try:
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, 'N/A')
            elif isinstance(data, list) and isinstance(key, int):
                if key < len(data):
                    data = data[key]
                else:
                    return 'N/A'
            else:
                return 'N/A'
        return data
    except (IndexError, KeyError, TypeError):
        return 'N/A'
    return 'N/A'

# Full field mapping based on the provided JSON structure
FIELD_MAPPING = {
    # 1. INFORMATION SUR L'ENTREPRISE
    "Nom du site à auditer": ["companyName"],
    "N° COID du portail": ["companyCoid"],
    "Code GLN": ["companyGlnNumber"],
    "Rue": ["companyStreetNo"],
    "Code postal": ["companyZip"],
    "Nom de la ville": ["companyCity"],
    "Pays": ["companyCountry"],
    "Téléphone": ["companyTelephone"],
    "Latitude": ["companyGpsLatitude"],
    "Longitude": ["companyGpsLongitude"],
    "Email": ["companyEmail"],
    
    # 2. Organisation de l'entreprise et de l'audit
    "Nom du siège social": ["headquartersName"],
    "Rue (siège social)": ["headquartersStreetNo"],
    "Nom de la ville (siège social)": ["headquartersCity"],
    "Code postal (siège social)": ["headquartersZip"],
    "Pays (siège social)": ["headquartersCountry"],
    "Téléphone (siège social)": ["headquartersTelephone"],

    # 3. ORGANISATION DU SITE
    "Surface couverte de l'entreprise (m²)": ["productionAreaSize"],
    "Nombre de bâtiments": ["numberOfBuildings"],
    "Nombre de lignes de production": ["numberOfProductionLines"],
    "Nombre d'étages": ["numberOfFloors"],
    "Nombre maximum d'employés dans l'année, au pic de production": ["numberOfEmployeesForTimeCalculation"],
    "Langue parlée et écrite sur le site": ["workingLanguage"],

    # 4. PRODUITS CONCERNES ET CHAMP DE L'AUDIT
    "Norme souhaitée": ["previousCertificationStandardVersion"],
    "Périmètre de l'audit": ["scopeCertificateScopeDescription"],
    "Process et activités": ["scopeProductGroupsDescription"],
    "Activité saisonnière ? (O/N)": ["seasonalProduction"],
    "Une partie du procédé de fabrication est-elle sous traitée? (OUI/NON)": ["partlyOutsourcedProcesses"],
    "Si oui lister les procédés sous-traités": ["partlyOutsourcedProcessesDescription"],
    "Avez-vous des produits totalement sous-traités? (OUI/NON)": ["fullyOutsourcedProducts"],
    "Si oui, lister les produits totalement sous-traités": ["fullyOutsourcedProductsDescription"],
    "Avez-vous des produits de négoce? (OUI/NON)": ["tradedProductsBrokerActivity"],
    "Si oui, lister les produits de négoce": ["tradedProductsBrokerActivityDescription"],
    "Produits à exclure du champ d'audit (OUI/NON)": ["exclusions"],
    "Préciser les produits à exclure": ["exclusionsDescription"]
}

# Custom CSS for the table
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
            white-space: pre-wrap;  /* This allows line breaks */
        }
        th {
            background-color: #f2f2f2;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Function to display the extracted data as an HTML table with proper formatting
def display_extracted_data(data_dict):
    apply_table_css()
    table_html = "<table><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>"
    for field, value in data_dict.items():
        table_html += f"<tr><td>{field}</td><td>{value}</td></tr>"
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)

# Step 1: Upload the JSON (.ifs) file
uploaded_json_file = st.file_uploader("Upload JSON (IFS) file", type="ifs")

if uploaded_json_file:
    try:
        # Step 2: Load the uploaded JSON file
        json_data = json.load(uploaded_json_file)

        # Step 3: Extract data from JSON based on the predefined mapping
        extracted_data = {}

        if isinstance(json_data, dict):
            for label, path in FIELD_MAPPING.items():
                extracted_data[label] = extract_nested_data(json_data, path)

            # Step 4: Display the extracted data as an HTML table
            st.title("Extracted Data from JSON (IFS)")
            display_extracted_data(extracted_data)
        else:
            st.error("Unexpected JSON structure. Please ensure the uploaded file has the correct format.")

    except json.JSONDecodeError:
        st.error("Error decoding the JSON file. Please ensure it is in the correct format.")
else:
    st.write("Please upload a JSON file in .ifs format to proceed.")

# Updates Summary:
# 1. Updated to filter only explicitly mapped fields based on the provided table.
# 2. Removed the JSON structure debugging display for a cleaner user experience.
# 3. Refined the extraction to only include necessary fields mapped in FIELD_MAPPING.


