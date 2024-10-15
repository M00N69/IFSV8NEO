import json
import pandas as pd
import streamlit as st

# Step 1: Load the CSV Checklist from the provided URL
@st.cache_data
def load_checklist(url):
    return pd.read_csv(url, sep=";")

# Step 2: Upload the JSON file and load the CSV file
uploaded_file_json = st.file_uploader("Upload JSON file", type="json")
checklist_url = "https://raw.githubusercontent.com/M00N69/Action-planGroq/main/Guide%20Checklist_IFS%20Food%20V%208%20-%20CHECKLIST.csv"

if uploaded_file_json:
    try:
        # Step 3: Load the JSON and Checklist
        data = json.load(uploaded_file_json)
        checklist_df = load_checklist(checklist_url)

        # Step 4: Check if the expected 'data' and 'modules' keys exist
        if "data" in data and "modules" in data["data"] and "food_8" in data["data"]["modules"]:
            food_8 = data['data']['modules']['food_8']

            # Extract data for overall results and matrix
            overall_result = food_8['result']['overall']
            matrix_result = food_8['matrixResult']
            
            # Step 5: Extract relevant columns from the checklist
            checklist_columns = ["NUM_REQ", "CHAPITRE", "QUESTION"]
            checklist_filtered = checklist_df[checklist_columns]

            # Step 6: Sidebar for navigation and chapter selection
            st.sidebar.title("Audit Sections")
            section = st.sidebar.radio("Select a section to view", ["Overall Results", "Chapters & Scores", "Requirements & Non-Conformities"])

            # Filter chapters based on the checklist data
            unique_chapters = sorted(set(checklist_filtered["CHAPITRE"]))
            selected_chapter = st.sidebar.selectbox("Select Chapter", unique_chapters)

            # Filter requirements by the selected chapter
            chapter_requirements = checklist_filtered[checklist_filtered["CHAPITRE"] == selected_chapter]

            # Step 7: Display filtered requirements from the checklist
            st.subheader(f"Requirements for Chapter {selected_chapter}")
            st.dataframe(chapter_requirements)

            # Step 8: Match JSON requirements with the checklist
            requirement_ids = chapter_requirements["NUM_REQ"].tolist()
            filtered_matrix = [item for item in matrix_result if str(item.get("chapterId")) == str(selected_chapter) and item.get("scoreId") in requirement_ids]

            # Display corresponding filtered requirements from the JSON
            st.subheader(f"Filtered Requirements from Audit Results for Chapter {selected_chapter}")
            if filtered_matrix:
                st.json(filtered_matrix)
            else:
                st.write("No matching requirements found in the audit data for this chapter.")
            
    except json.JSONDecodeError:
        st.error("The file could not be decoded as a JSON. Please check the file format.")
else:
    st.write("Please upload the JSON file to begin.")







