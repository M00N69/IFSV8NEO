import json
import streamlit as st

# Step 1: Upload the JSON file
uploaded_file = st.file_uploader("Upload JSON file", type="json")

if uploaded_file:
    try:
        # Step 2: Load the uploaded JSON file
        data = json.load(uploaded_file)
        
        # Step 3: Display the top-level structure of the JSON file
        st.header("JSON File Structure")
        st.write("Top-level keys in the JSON:")
        st.json(data)  # This will display the structure of the uploaded JSON

        # Step 4: Optionally list the keys at the top level
        if isinstance(data, dict):
            top_level_keys = list(data.keys())
            st.write(f"Top-level keys: {top_level_keys}")
        else:
            st.error("The uploaded file does not seem to be a valid JSON object.")
        
    except json.JSONDecodeError:
        st.error("The file could not be decoded as a JSON. Please check the file format.")




