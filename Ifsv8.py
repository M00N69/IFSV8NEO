import streamlit as st
import json

# Fonction pour charger le fichier JSON
def load_json(file):
    return json.load(file)

# Fonction pour sauvegarder les modifications dans un fichier JSON
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Fonction pour ajouter des commentaires dans un fichier séparé
def add_comment(comment_data, comments_file='comments.json'):
    try:
        with open(comments_file, 'r') as f:
            comments = json.load(f)
    except FileNotFoundError:
        comments = {}

    comments.update(comment_data)
    with open(comments_file, 'w') as f:
        json.dump(comments, f, indent=4)

# Interface principale
st.title('Analyse d'Audit IFS')

uploaded_file = st.file_uploader("Choisissez un fichier IFS (.json)", type="json")

if uploaded_file is not None:
    # Charger et afficher le fichier JSON
    data = load_json(uploaded_file)
    
    # Meta information
    st.subheader('Informations générales')
    st.json({
        "hash": data.get("hash"),
        "schemaVersion": data.get("schemaVersion"),
        "axpxVersion": data.get("axpxVersion"),
        "moduleDefinitionVersion": data.get("moduleDefinitionVersion")
    })

    # Navigation entre les chapitres
    st.subheader('Navigation des chapitres')
    matrix_result = data.get("data", {}).get("modules", {}).get("food_8", {}).get("matrixResult", [])
    chapter_ids = [chapter.get("chapterId", "") for chapter in matrix_result]
    selected_chapter = st.selectbox("Choisissez un chapitre", chapter_ids)
    
    # Afficher le chapitre sélectionné
    for chapter in matrix_result:
        if chapter.get("chapterId") == selected_chapter:
            st.write(f"Chapitre ID: {selected_chapter}")
            st.json(chapter)
            break

    # Visualisation des non-conformités
    st.subheader('Non-conformités')
    checklist = data.get("data", {}).get("modules", {}).get("food_8", {}).get("checklists", {}).get("checklistFood8", {}).get("requirements", [])
    non_conformities = [req for req in checklist if req.get("score") in ["C", "D", "MAJOR", "KO"]]
    
    if non_conformities:
        st.write(f"Nombre de non-conformités: {len(non_conformities)}")
        comments_to_save = {}
        for nc in non_conformities:
            st.write(f"Requirement UUID: {nc.get('requirementUuid')}")
            st.write(f"Score: {nc.get('score')}")
            st.write(f"Explication: {nc.get('explanationText', 'Non disponible')}")
            # Ajouter un commentaire pour la non-conformité
            comment = st.text_area(f"Ajouter un commentaire pour la requirement {nc.get('requirementUuid')}", key=nc.get('requirementUuid'))
            comments_to_save[nc.get('requirementUuid')] = comment
        
        # Enregistrer tous les commentaires
        if st.button("Enregistrer tous les commentaires"):
            add_comment(comments_to_save)
            st.success("Tous les commentaires ont été enregistrés avec succès !")
    else:
        st.write("Aucune non-conformité trouvée.")

    # Sauvegarder les modifications avec vérification de la structure
    if st.button('Enregistrer les modifications'):
        try:
            # Vérification de la structure avant sauvegarde
            save_json(data, 'modified_audit.json')
            st.success('Fichier JSON sauvegardé avec succès !')
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde : {e}")
