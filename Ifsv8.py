import json
import streamlit as st

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
        # If it's a primitive, we add it directly
        items.append((parent_key, nested_json))
    return dict(items)

# Function to extract data from the flattened JSON
def extract_from_flattened(flattened_data, mapping):
    extracted_data = {}
    for label, flat_path in mapping.items():
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

# Function to display the extracted data as an HTML table
def display_extracted_data(extracted_data):
    apply_table_css()
    table_html = "<table><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>"
    for field, value in extracted_data.items():
        table_html += f"<tr><td>{field}</td><td>{value}</td></tr>"
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)

# Complete mapping based on your provided field names and JSON structure
FLATTENED_FIELD_MAPPING = {
    "Follow-up Summary Answer": "data_modules_food_8_questions_followupSummary_answer",
    "Follow-up Summary Revision": "data_modules_food_8_questions_followupSummary_revision",
    "KO Summary Answer": "data_modules_food_8_questions_koSummary_answer",
    "KO Summary Revision": "data_modules_food_8_questions_koSummary_revision",
    "Scope Certificate Description (EN)": "data_modules_food_8_questions_scopeCertificateScopeDescription_en_answer",
    "Scope Certificate Revision": "data_modules_food_8_questions_scopeCertificateScopeDescription_en_revision",
    "Company COID Answer": "data_modules_food_8_questions_companyCoid_answer",
    "Company COID Revision": "data_modules_food_8_questions_companyCoid_revision",
    "Company Name Answer": "data_modules_food_8_questions_companyName_answer",
    "Company Name Revision": "data_modules_food_8_questions_companyName_revision",
    "Company Street Number Answer": "data_modules_food_8_questions_companyStreetNo_answer",
    "Company Street Number Revision": "data_modules_food_8_questions_companyStreetNo_revision",
    "Company ZIP Answer": "data_modules_food_8_questions_companyZip_answer",
    "Company ZIP Revision": "data_modules_food_8_questions_companyZip_revision",
    "Company City Answer": "data_modules_food_8_questions_companyCity_answer",
    "Company City Revision": "data_modules_food_8_questions_companyCity_revision",
    "Company Telephone Answer": "data_modules_food_8_questions_companyTelephone_answer",
    "Company Telephone Revision": "data_modules_food_8_questions_companyTelephone_revision",
    "Company Email Answer": "data_modules_food_8_questions_companyEmail_answer",
    "Company Email Revision": "data_modules_food_8_questions_companyEmail_revision",
    "Company Webpage Answer": "data_modules_food_8_questions_companyWebpage_answer",
    "Company Webpage Revision": "data_modules_food_8_questions_companyWebpage_revision",
    "Company GPS Latitude Answer": "data_modules_food_8_questions_companyGpsLatitude_answer",
    "Company GPS Latitude Revision": "data_modules_food_8_questions_companyGpsLatitude_revision",
    "Company GPS Longitude Answer": "data_modules_food_8_questions_companyGpsLongitude_answer",
    "Company GPS Longitude Revision": "data_modules_food_8_questions_companyGpsLongitude_revision",
    # Continue mapping for all required fields in similar fashion
}

# Streamlit app
st.title("IFS File Uploader and Data Extractor")

# Step 1: Upload the JSON (.ifs) file
uploaded_json_file = st.file_uploader("Upload JSON (IFS) file", type="ifs")

if uploaded_json_file:
    try:
        # Step 2: Load the uploaded JSON file
        json_data = json.load(uploaded_json_file)

        # Step 3: Flatten the JSON data
        flattened_json_data_safe = flatten_json_safe(json_data)

        # Step 4: Extract the required data based on the mapping
        extracted_data = extract_from_flattened(flattened_json_data_safe, FLATTENED_FIELD_MAPPING)

        # Step 5: Display the extracted data as an HTML table
        st.subheader("Extracted Data")
        display_extracted_data(extracted_data)

    except json.JSONDecodeError:
        st.error("Error decoding the JSON file. Please ensure it is in the correct format.")
else:
    st.write("Please upload a JSON (.ifs) file to proceed.")




