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

        # Check if the expected 'data' and 'modules' keys exist
        if "data" in data and "modules" in data["data"] and "food_8" in data["data"]["modules"]:
            food_8 = data['data']['modules']['food_8']
            
            # Extract data for overall results and matrix
            overall_result = food_8['result']['overall']
            matrix_result = food_8['matrixResult']
            
            # Step 4: Display Overall Audit Results
            st.title("Audit Overview")
            st.write(f"Audit Level: {overall_result['level']}")
            st.write(f"Audit Passed: {overall_result['passed']}")
            st.write(f"Audit Percentage: {overall_result['percent']}%")

            # Step 5: Sidebar for navigation
            st.sidebar.title("Audit Sections")
            section = st.sidebar.radio("Select a section to view", ["Overall Results", "Chapters & Scores", "Requirements & Non-Conformities"])

            # Chapter-wise, Section, and Subsection-wise Results Section
            if section == "Chapters & Scores":
                st.header("Chapter, Section, and Subsection-wise Scores and Compliance")
                
                # Get unique chapters, sections, and subsections from the CSV file
                unique_chapters = sorted(checklist_df["CHAPITRE"].unique())
                selected_chapter = st.selectbox("Select a Chapter", unique_chapters)

                # Filter sections based on the selected chapter
                chapter_sections = checklist_df[checklist_df["CHAPITRE"] == selected_chapter]
                unique_sections = sorted(chapter_sections["SECTION"].unique())
                selected_section = st.selectbox("Select a Section", unique_sections)

                # Filter subsections based on the selected section
                section_subsections = chapter_sections[chapter_sections["SECTION"] == selected_section]
                unique_subsections = sorted(section_subsections["SOUS_SECTION"].unique())
                selected_subsection = st.selectbox("Select a Subsection", unique_subsections)

                # Display filtered requirements from the checklist
                filtered_requirements = section_subsections[section_subsections["SOUS_SECTION"] == selected_subsection]
                st.subheader(f"Requirements for Chapter {selected_chapter}, Section {selected_section}, Subsection {selected_subsection}")
                st.dataframe(filtered_requirements)

                # Extract corresponding requirements from the JSON based on NUM_REQ from the checklist
                requirement_ids = filtered_requirements["NUM_REQ"].tolist()
                chapter_data = [item for item in matrix_result if item['chapterId'] == str(selected_chapter) and item['scoreId'] in requirement_ids]

                if chapter_data:
                    st.subheader(f"Scores for Chapter {selected_chapter}")

                    # Convert the data to a DataFrame for better visualization
                    df = pd.DataFrame(chapter_data)
                    
                    # Select the columns we want to display in the table
                    df_filtered = df[['type', 'levelId', 'chapterId', 'scoreId', 'count']]

                    # Display the data as a table with custom CSS
                    st.dataframe(df_filtered)

                # Filter for non-conformities
                if st.checkbox("Show Non-Conformities Only"):
                    non_conformities = [item for item in matrix_result if item['chapterId'] == str(selected_chapter) and item['scoreId'] in ['C', 'D', 'MAJOR', 'KO']]
                    if non_conformities:
                        df_nc = pd.DataFrame(non_conformities)
                        st.subheader("Non-conformities in the selected chapter:")
                        st.dataframe(df_nc[['type', 'scoreId', 'count']])
                    else:
                        st.write("No non-conformities found in the selected chapter.")

            # Requirements and Non-conformities Section
            elif section == "Requirements & Non-Conformities":
                st.header("Requirements, Scores, and Non-Conformities")

                # Extract requirements and scores (Assuming this part is structured like the previous part)
                checklists = food_8['checklists']['checklistFood8']['resultScorings']
                
                # Now link the NUM_REQ from the CSV with the JSON requirement IDs
                csv_num_reqs = checklist_df["NUM_REQ"].tolist()
                requirement_ids = list(set(checklists.keys()) & set(csv_num_reqs))
                
                selected_requirement = st.selectbox("Select a Requirement (NUM_REQ)", requirement_ids)

                # Display details of the selected requirement
                if selected_requirement:
                    req_data = checklists[selected_requirement]
                    st.subheader(f"Requirement ID: {selected_requirement}")
                    st.write(f"Score: {req_data['score']['label']} ({req_data['score']['value']})")
                    st.write("Explanation:")
                    st.text(req_data['answers']['explanationText'] if req_data['answers']['explanationText'] else "No explanation provided.")

                    # Show non-conformities if any
                    if req_data['isCorrectionRequired']:
                        st.warning("Non-conformity found!")
                        st.write(req_data['answers']['explanationText'])

                    # Expand to show additional details
                    with st.expander("Show additional information"):
                        st.write(f"English Explanation: {req_data['answers']['englishExplanationText']}")

            # Show Data Filters (Non-conformities across all chapters)
            st.sidebar.subheader("Filter Non-Conformities")
            show_non_conformities = st.sidebar.checkbox("Show All Non-conformities")

            if show_non_conformities:
                st.header("All Non-conformities Across the Audit")
                all_non_conformities = [item for item in matrix_result if item.get('scoreId') in ['C', 'D', 'MAJOR', 'KO']]
                if all_non_conformities:
                    df_all_nc = pd.DataFrame(all_non_conformities)
                    st.dataframe(df_all_nc[['type', 'levelId', 'chapterId', 'scoreId', 'count']])
                else:
                    st.write("No non-conformities found across the audit.")

        else:
            st.error("The expected 'data', 'modules', or 'food_8' key does not exist in the uploaded JSON.")

    except json.JSONDecodeError:
        st.error("The file could not be decoded as a JSON. Please check the file format.")

else:
    st.write("Please upload a JSON file to begin.")









