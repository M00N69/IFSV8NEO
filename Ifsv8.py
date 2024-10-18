import json
import streamlit as st

# Function to extract nested data safely, handling lists when necessary
def extract_nested_data(data, keys):
    """Recursively extract data from a nested dictionary, handling lists."""
    try:
        if isinstance(data, dict):
            return data.get(keys[0], 'N/A') if len(keys) == 1 else extract_nested_data(data.get(keys[0], {}), keys[1:])
        elif isinstance(data, list) and isinstance(keys[0], int):
            return data[keys[0]] if len(keys) == 1 else extract_nested_data(data[keys[0]], keys[1:])
    except (IndexError, KeyError, TypeError):
        return 'N/A'
    return 'N/A'

# Full field mapping based on the provided JSON structure
FIELD_MAPPING = {
    # Updated FIELD_MAPPING based on the uploaded file structure
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
    "Nom du siège social": ["headquartersName"],
    "Rue (siège social)": ["headquartersStreetNo"],
    "Nom de la ville (siège social)": ["headquartersCity"],
    "Code postal (siège social)": ["headquartersZip"],
    "Pays (siège social)": ["headquartersCountry"],
    "Téléphone (siège social)": ["headquartersTelephone"],
    "Surface couverte de l'entreprise (m²)": ["productionAreaSize"],
    "Nombre de bâtiments": ["numberOfBuildings"],
    "Nombre de lignes de production": ["numberOfProductionLines"],
    "Nombre d'étages": ["numberOfFloors"],
    "Nombre maximum d'employés dans l'année, au pic de production": ["numberOfEmployeesForTimeCalculation"],
    "Langue parlée et écrite sur le site": ["workingLanguage"],
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

        for label, path in FIELD_MAPPING.items():
            extracted_data[label] = extract_nested_data(json_data, path)

        # Step 4: Display the extracted data as an HTML table
        st.title("Extracted Data from JSON (IFS)")
        display_extracted_data(extracted_data)

    except json.JSONDecodeError:
        st.error("Error decoding the JSON file. Please ensure it is in the correct format.")
else:
    st.write("Please upload a JSON file in .ifs format to proceed.")

# Updates Summary:
# 1. Updated FIELD_MAPPING: The FIELD_MAPPING has been updated to correctly match the actual structure of the JSON file based on the provided image.
# 2. Updated Nested Keys for Extraction: The extract_nested_data function was retained and used to match the updated paths.
# 3. The updated FIELD_MAPPING keys now accurately reflect the structure of the JSON data, ensuring proper extraction of the required fields.
# 4. Code includes detailed comments explaining the function of each section and how the nested extraction works.

# Notes:
# The FIELD_MAPPING is based on the provided data from the image and may still require tweaking if there are additional fields or changes in the JSON structure.






