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

        # Extract required fields from the JSON file
        general_info = {
            "Company Name": data['questions']['companyName']['answer'],
            "Audit Date": data['questions']['auditLastDay']['answer'],
            "Audit Type": data['questions']['executionMode']['answer'],
            "Certificate Issued": data['questions']['certificateIsIssued']['answer'],
            "Headquarters": data['questions']['headquartersStreetNo']['answer'],
            "City": data['questions']['headquartersCity']['answer'],
            "Country": data['questions']['headquartersCountry']['answer'][0],
            "Telephone": data['questions']['headquartersTelephone']['answer'],
            "Email": data['questions']['headquartersEmail']['answer'],
            "Company Website": data['questions']['headquartersWebpage']['answer'],
            "Certification Body": data['questions']['certificationBodyName']['answer'],
            "Certification Body Address": data['questions']['certificationBodyAddress']['answer'],
        }

        contact_person = {
            "Contact Person": data['questions']['headquartersContactPersonName']['answer'],
            "Contact Email": data['questions']['companyEmergencyContactEmail']['answer'],
            "Emergency Contact Telephone": data['questions']['companyEmergencyContactTelephone']['answer'],
        }

        technological_scope = {
            "Technological Scope": data['scopeAuditScopeDescription']['answer'],
            "Product Groups Description": data['scopeProductGroupsDescription']['answer'],
        }

        process_info = {
            "Processes Involved": data['productsProducedProcessesRunning_en']['answer'],
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
