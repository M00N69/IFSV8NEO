import json
import pandas as pd
import streamlit as st

# Step 1: Load the IFS v8 Checklist from Excel
@st.cache_data
def load_checklist(file):
    return pd.read_excel(file)

# Step 2: Upload the JSON and Excel files
uploaded_file_json = st.file_uploader("Upload JSON file", type="json")
uploaded_file_excel = st.file_uploader("Upload IFS v8 Checklist", type="xlsx")

if uploaded_file_json and uploaded_file_excel:
    try:
        # Step 3: Load the JSON and Excel files
        data = json.load(uploaded_file_json)
        checklist_df = load_checklist(uploaded_file_excel)

        # Step 4: Check if the expected 'data' and 'modules' keys exist
        if "data" in data and "modules" in data["data"] and "food_8" in data["data"]["modules"]:
            food_8 = data['data']['modules']['food_8']

            # Extract data for overall results and matrix
            overall_result = food_8['result']['overall']
            matrix_result = food_8['matrixResult']
            
            # Extract relevant columns from the checklist for chapter-wise filtering
            checklist_columns = ["Chapter", "Requirement ID", "Requirement Description"]
            checklist_filtered = checklist_df[checklist_columns]

            # Step 5: Sidebar for navigation and chapter selection
            st.sidebar.title("Audit Sections")
            section = st.sidebar.radio("Select a section to view", ["Overall Results", "Chapters & Scores", "Requirements & Non-Conformities"])

            # Chapter filtering
            unique_chapters = sorted(set(checklist_filtered["Chapter"]))
            selected_chapter = st.sidebar.selectbox("Select Chapter", unique_chapters)

            # Filter requirements by selected chapter
            chapter_requirements = checklist_filtered[checklist_filtered["Chapter"] == selected_chapter]

            # Display filtered requirements
            st.subheader(f"Requirements for Chapter {selected_chapter}")
            st.dataframe(chapter_requirements)

            # Step 6: Link the filtered chapter to the corresponding requirements in the JSON data
            requirement_ids = chapter_requirements["Requirement ID"].tolist()
            filtered_matrix = [item for item in matrix_result if item["chapterId"] == str(selected_chapter) and item.get("scoreId") in requirement_ids]

            # Display corresponding filtered requirements in the JSON
            st.subheader("Filtered Requirements from Audit Results")
            if filtered_matrix:
                st.json(filtered_matrix)
            else:
                st.write("No matching requirements found in the audit data for this chapter.")
            
    except json.JSONDecodeError:
        st.error("The file could not be decoded as a JSON. Please check the file format.")
else:
    st.write("Please upload both the JSON and IFS v8 Checklist files to begin.")






