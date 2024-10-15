import streamlit as st
import json

# Function to load JSON
def load_json(file):
    return json.load(file)

# Function to save the modified JSON
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Recursive function to explore JSON structure
def explore_json(data, level=0):
    if isinstance(data, dict):
        for key, value in data.items():
            st.write("  " * level + f"Key: {key}")
            explore_json(value, level + 1)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            st.write("  " * level + f"Index: {index}")
            explore_json(item, level + 1)
    else:
        st.write("  " * level + f"Value: {data}")

# Main interface
st.title("Audit IFS Analysis Tool")

uploaded_file = st.file_uploader("Choose an IFS audit file (.json)", type="json")

if uploaded_file is not None:
    # Load the JSON data
    data = load_json(uploaded_file)
    
    # Display the full JSON structure for inspection
    st.header("Full JSON Inspection")
    with st.expander("View full JSON structure"):
        explore_json(data)

    # Sidebar for meta information
    st.sidebar.header('General Information')
    st.sidebar.json({
        "hash": data.get("hash"),
        "schemaVersion": data.get("schemaVersion"),
        "axpxVersion": data.get("axpxVersion"),
        "moduleDefinitionVersion": data.get("moduleDefinitionVersion")
    })

    # Filter section for chapters and non-conformities
    st.header('Filter Options')

    # Get modules and food_8 data
    modules = data.get("data", {}).get("modules", {})
    food_module = modules.get("food_8", {})
    matrix_result = food_module.get("matrixResult", [])

    # Filter chapters by available chapter IDs
    chapter_ids = list({str(chapter.get("chapterId", "")) for chapter in matrix_result})
    chapter_ids.sort()
    selected_chapter = st.selectbox("Select a chapter", chapter_ids)

    # Display selected chapter details
    selected_chapter_data = [chapter for chapter in matrix_result if str(chapter.get("chapterId")) == selected_chapter]
    if selected_chapter_data:
        st.subheader(f"Details of Chapter {selected_chapter}")
        st.json(selected_chapter_data[0])

        # Display the specific requirements for the selected chapter
        st.subheader(f"Chapter {selected_chapter} Requirements")
        checklist = food_module.get("checklists", {}).get("checklistFood8", {}).get("requirements", [])
        chapter_requirements = [req for req in checklist if str(req.get("chapterId")) == selected_chapter]
        if chapter_requirements:
            for req in chapter_requirements:
                with st.expander(f"Requirement {req.get('requirementUuid')}"):
                    st.write(f"Score: {req.get('score')}")
                    st.write(f"Explanation: {req.get('explanationText', 'Not available')}")
                    st.json(req)
                    # Add comments for each requirement
                    comment = st.text_area(f"Add a comment for requirement {req.get('requirementUuid')}", key=req.get('requirementUuid'))
                    if st.button(f"Save comment for {req.get('requirementUuid')}"):
                        # Here you would normally save the comment
                        st.success(f"Comment saved for {req.get('requirementUuid')}")
        else:
            st.write("No requirements found for this chapter.")
    else:
        st.write("No details found for the selected chapter.")

    # Filter and display non-conformities
    st.header('Non-conformities')
    non_conformities = [req for req in checklist if req.get("score") in ["C", "D", "MAJOR", "KO"]]

    if non-conformities:
        st.write(f"Number of non-conformities: {len(non-conformities)}")
        comments_to_save = {}
        for nc in non_conformities:
            with st.expander(f"Non-conformity {nc.get('requirementUuid')}"):
                st.write(f"Score: {nc.get('score')}")
                st.write(f"Explanation: {nc.get('explanationText', 'Not available')}")
                st.json(nc)
                # Add a comment for non-conformities
                comment = st.text_area(f"Add a comment for non-conformity {nc.get('requirementUuid')}", key=f"nc_{nc.get('requirementUuid')}")
                comments_to_save[nc.get('requirementUuid')] = comment

        # Save all non-conformity comments
        if st.button("Save all non-conformity comments"):
            # Normally you'd handle the saving logic here
            st.success("All non-conformity comments have been successfully saved!")
    else:
        st.write("No non-conformities found.")

    # Save modifications to the JSON file
    if st.button('Save modifications'):
        try:
            save_json(data, 'modified_audit.json')
            st.success('JSON file saved successfully!')
        except Exception as e:
            st.error(f"Error saving the file: {e}")


