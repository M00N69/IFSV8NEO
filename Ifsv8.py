import json
import pandas as pd
import streamlit as st

# Custom CSS for enabling line breaks in table cells
def local_css():
    st.markdown(
        """
        <style>
        .dataframe td {
            white-space: pre-wrap;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Load custom CSS for line breaks
local_css()

# Step 1: Load the CSV Checklist from the provided URL with error handling
@st.cache_data
def load_checklist(url):
    try:
        # Load the CSV file with the necessary encoding and handling of bad lines
        return pd.read_csv(url, sep=";", encoding='utf-8', on_bad_lines='skip')
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV file: {e}")
        return None

checklist_url = "https://raw.githubusercontent.com/M00N69/Action-planGroq/main/Guide%20Checklist_IFS%20Food%20V%208%20-%20CHECKLIST.csv"
checklist_df = load_checklist(checklist_url)

# Step 2: Upload the JSON file
uploaded_file = st.file_uploader("Upload JSON file", type="json")

if uploaded_file and checklist_df is not None:
    try:
        # Step 3: Load the uploaded JSON file
        data = json.load(uploaded_file)

        # Extract required fields from the JSON file with safe access
        general_info = {
            "Company Name": data['questions'].get('companyName', {}).get('answer', 'N/A'),
            "Audit Date": data['questions'].get('auditLastDay', {}).get('answer', 'N/A'),
            "Audit Type": data['questions'].get('executionMode', {}).get('answer', 'N/A'),
            "Certificate Issued": data['questions'].get('certificateIsIssued', {}).get('answer', 'N/A'),
            "Headquarters": data['questions'].get('headquartersStreetNo', {}).get('answer', 'N/A'),
            "City": data['questions'].get('companyCity', {}).get('answer', 'N/A'),
            "Country": data['questions'].get('headquartersCountry', {}).get('answer', ['N/A'])[0],
            "Telephone": data['questions'].get('companyTelephone', {}).get('answer', 'N/A'),
            "Email": data['questions'].get('companyEmail', {}).get('answer', 'N/A'),
            "Company Website": data['questions'].get('headquartersWebpage', {}).get('answer', 'N/A'),
            "Certification Body": data['questions'].get('certificationBodyName', {}).get('answer', 'N/A'),
            "Certification Body Address": data['questions'].get('certificationBodyAddress', {}).get('answer', 'N/A'),
        }

        contact_person = {
            "Contact Person": data['questions'].get('headquartersContactPersonName', {}).get('answer', 'N/A'),
            "Contact Email": data['questions'].get('companyEmergencyContactEmail', {}).get('answer', 'N/A'),
            "Emergency Contact Telephone": data['questions'].get('companyEmergencyContactTelephone', {}).get('answer', 'N/A'),
        }

        technological_scope = {
            "Technological Scope": data['questions'].get('scopeAuditScopeDescription', {}).get('answer', 'N/A'),
            "Product Groups Description": data['questions'].get('scopeProductGroupsDescription', {}).get('answer', 'N/A'),
        }

        process_info = {
            "Processes Involved": data['questions'].get('productsProducedProcessesRunning_en', {}).get('answer', 'N/A'),
        }

        # Step 4: Display General Information
        st.title("General Site Information")
        st.write(pd.DataFrame(general_info.items(), columns=['Field', 'Information']))

        # Step 5: Display Contact Information
        st.title("Contact Person Information")
        st.write(pd.DataFrame(contact_person.items(), columns=['Field', 'Information']))

        # Step 6: Display Technological Scopes
        st.title("Technological Scope")
        st.write(pd.DataFrame(technological_scope.items(), columns=['Field', 'Description']))

        # Step 7: Display Processes Information
        st.title("Processes Involved")
        st.write(pd.DataFrame(process_info.items(), columns=['Field', 'Details']))

    except json.JSONDecodeError:
        st.error("The file could not be decoded as a JSON. Please check the file format.")

else:
    st.write("Please upload a JSON file to begin.")

