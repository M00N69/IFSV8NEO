import json
import pandas as pd
import streamlit as st

# Step 1: Function to read the Excel file and create the field mapping
@st.cache_data
def load_excel_mapping(file):
    try:
        df = pd.read_excel(file, sheet_name=0)
        # Assuming first column has labels and second column has JSON keys
        field_mapping = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        return field_mapping
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

# Step 2: Upload JSON (.ifs) and Excel files
uploaded_json_file = st.file_uploader("Upload JSON (IFS) file", type="ifs")
uploaded_excel_file = st.file_uploader("Upload Excel mapping file", type="xlsx")

if uploaded_json_file and uploaded_excel_file:
    try:
        # Step 3: Load the JSON data
        json_data = json.load(uploaded_json_file)
        
        # Step 4: Load the Excel field mapping
        field_mapping = load_excel_mapping(uploaded_excel_file)

        if field_mapping:
            extracted_data = {}

            # Step 5: Extract data from JSON based on the Excel mapping
            for label, json_key in field_mapping.items():
                if json_key and json_key in json_data.get('questions', {}):
                    extracted_data[label] = json_data['questions'].get(json_key, {}).get('answer', 'N/A')
                else:
                    extracted_data[label] = 'N/A'

            # Step 6: Create a DataFrame from the extracted data
            extracted_df = pd.DataFrame(list(extracted_data.items()), columns=["Field", "Value"])
            
            # Step 7: Display the DataFrame in Streamlit
            st.title("Extracted Data")
            st.write(extracted_df)

            # Step 8: Provide option to download the extracted data as Excel
            def convert_df_to_excel(df):
                return df.to_excel(index=False, engine='xlsxwriter')

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
    st.write("Please upload both the JSON (IFS) file and the Excel mapping file to proceed.")

