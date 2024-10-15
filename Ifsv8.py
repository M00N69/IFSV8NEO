import json
import streamlit as st

# Load JSON data from uploaded file
uploaded_file = st.file_uploader("Upload JSON file", type="json")

if uploaded_file:
    data = json.load(uploaded_file)
    
    # Extract necessary components
    overall_result = data['modules']['food_8']['result']['overall']
    matrix_result = data['modules']['food_8']['matrixResult']
    checklists = data['modules']['food_8']['checklists']['checklistFood8']['resultScorings']

    # Display Overall Audit Result
    st.title("Audit Overview")
    st.write(f"Audit Level: {overall_result['level']}")
    st.write(f"Audit Passed: {overall_result['passed']}")
    st.write(f"Audit Percentage: {overall_result['percent']}%")

    # Sidebar for navigation
    st.sidebar.title("Audit Sections")
    section = st.sidebar.radio("Select a section to view", ["Overall Results", "Chapters & Scores", "Requirements & Non-Conformities"])

    # Overall Results Section
    if section == "Overall Results":
        st.header("Overall Audit Results")
        st.json(overall_result)
    
    # Chapter-wise Results Section
    elif section == "Chapters & Scores":
        st.header("Chapter-wise Scores and Compliance")
        # List available chapters based on matrixResult
        chapters = [f"Chapter {item['chapterId']}" for item in matrix_result if "chapterId" in item]
        selected_chapter = st.selectbox("Select a Chapter", chapters)
        
        # Display chapter scores
        chapter_data = [item for item in matrix_result if f"Chapter {item['chapterId']}" == selected_chapter]
        
        if chapter_data:
            st.subheader(f"Scores for {selected_chapter}")
            st.write(f"Percentage: {chapter_data[0].get('percentage', 'N/A')}%")
            st.json(chapter_data)

        # Filter for scores and compliance
        if st.checkbox("Show Non-Conformities Only"):
            non_conformities = [item for item in matrix_result if item.get('scoreId') in ['C', 'D', 'MAJOR', 'KO']]
            st.write("Non-conformities in selected chapter:")
            st.json(non_conformities)

    # Requirements and Non-conformities Section
    elif section == "Requirements & Non-Conformities":
        st.header("Requirements, Scores, and Non-Conformities")
        
        # Select requirement based on available IDs in checklists
        requirement_ids = list(checklists.keys())
        selected_requirement = st.selectbox("Select a Requirement", requirement_ids)

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
            st.json(all_non_conformities)
        else:
            st.write("No non-conformities found!")



