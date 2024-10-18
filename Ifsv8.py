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

# Function to display the JSON structure for debugging purposes
def display_json_structure(json_data, prefix=""):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            st.write(f"{prefix}{key}")
            display_json_structure(value, prefix=prefix + "  ")
    elif isinstance(json_data, list):
        for i, item in enumerate(json_data):
            st.write(f"{prefix}[{i}]")
            display_json_structure(item, prefix=prefix + "  ")

# Step 1: Upload the JSON (.ifs) file
uploaded_json_file = st.file_uploader("Upload JSON (IFS) file", type="ifs")

if uploaded_json_file:
    try:
        # Step 2: Load the uploaded JSON file
        json_data = json.load(uploaded_json_file)

        # Step 3: Display JSON structure for debugging
        st.subheader("JSON Structure Preview")
        display_json_structure(json_data)

        # Step 4: Extract data from JSON based on the predefined mapping
        extracted_data = {}

        # Assuming the JSON has multiple entries, iterate through each key-value pair
        for key, value in json_data.items():
            entry_data = {}
            for label, path in FIELD_MAPPING.items():
                entry_data[label] = extract_nested_data(value, path)
            extracted_data[key] = entry_data

        # Step 5: Display the extracted data as an HTML table for each entry
        st.title("Extracted Data from JSON (IFS)")
        for key, data in extracted_data.items():
            st.subheader(f"Entry ID: {key}")
            display_extracted_data(data)

    except json.JSONDecodeError:
        st.error("Error decoding the JSON file. Please ensure it is in the correct format.")
else:
    st.write("Please upload a JSON file in .ifs format to proceed.")

# Updates Summary:
# 1. Expanded FIELD_MAPPING: The FIELD_MAPPING has been updated to include all relevant fields as per the provided image.
# 2. Added JSON Structure Preview: Added a function to display the JSON structure to help with debugging and identifying correct paths.
# 3. Updated Nested Keys for Extraction: The extract_nested_data function was retained and used to match the updated paths.
# 4. The updated FIELD_MAPPING keys now accurately reflect the structure of the JSON data, ensuring proper extraction of the required fields.
# 5. Code includes detailed comments explaining the function of each section and how the nested extraction works.
# 6. Iteration over Entries: The code now iterates over each entry in the JSON to extract relevant data.




