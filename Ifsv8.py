import streamlit as st
import json

# Fonction pour charger le fichier JSON
def load_json(file):
    return json.load(file)

# Fonction pour sauvegarder les modifications dans un fichier JSON
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Fonction récursive pour explorer et afficher la structure complète du JSON
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

# Interface principale
st.title("Analyse d'Audit IFS")

uploaded_file = st.file_uploader("Choisissez un fichier IFS (.json)", type="json")

if uploaded_file is not None:
    # Charger et afficher le fichier JSON
    data = load_json(uploaded_file)
    
    # Afficher l'intégralité du fichier JSON pour inspection
    st.header("Inspection complète du fichier JSON")
    with st.expander("Voir la structure complète du fichier JSON"):
        explore_json(data)
    
    # Meta information dans une section dédiée
    st.sidebar.header('Informations générales')
    st.sidebar.json({
        "hash": data.get("hash"),
        "schemaVersion": data.get("schemaVersion"),
        "axpxVersion": data.get("axpxVersion"),
        "moduleDefinitionVersion": data.get("moduleDefinitionVersion")
    })

    # Navigation entre les chapitres
    st.header('Navigation des chapitres')
    modules = data.get("data", {}).get("modules", {})
    food_module = modules.get("food_8", {})
    matrix_result = food_module.get("matrixResult", [])
    chapter_ids = list({str(chapter.get("chapterId", "")) for chapter in matrix_result})  # Utiliser un set pour éliminer les doublons puis convertir en liste
    chapter_ids.sort()  # Trier les chapitres pour une meilleure lisibilité
    selected_chapter = st.selectbox("Choisissez un chapitre", chapter_ids)
    
    # Afficher le chapitre sélectionné et ses exigences dans une mise en page plus lisible
    selected_chapter_data = [chapter for chapter in matrix_result if str(chapter.get("chapterId")) == selected_chapter]
    if selected_chapter_data:
        st.subheader(f"Détails du Chapitre {selected_chapter}")
        st.write(f"Chapitre ID: {selected_chapter}")
        st.json(selected_chapter_data[0])

        # Afficher les exigences du chapitre sélectionné de manière structurée
        st.subheader(f"Exigences du Chapitre {selected_chapter}")
        checklist = food_module.get("checklists", {}).get("checklistFood8", {}).get("requirements", [])
        chapter_requirements = [req for req in checklist if str(req.get("chapterId")) == selected_chapter]
        if chapter_requirements:
            for req in chapter_requirements:
                with st.expander(f"Exigence {req.get('requirementUuid')}"):
                    st.write(f"Score: {req.get('score')}")
                    st.write(f"Explication: {req.get('explanationText', 'Non disponible')}")
                    st.json(req)  # Afficher tous les détails de l'exigence de manière arborescente
                    # Ajouter un commentaire pour chaque exigence
                    comment = st.text_area(f"Ajouter un commentaire pour la requirement {req.get('requirementUuid')}", key=req.get('requirementUuid'))
                    if st.button(f"Enregistrer le commentaire pour {req.get('requirementUuid')}"):
                        add_comment({req.get('requirementUuid'): comment})
                        st.success(f"Commentaire enregistré pour {req.get('requirementUuid')}")
        else:
            st.write("Aucune exigence trouvée pour ce chapitre.")
    else:
        st.write("Aucun détail trouvé pour le chapitre sélectionné.")

    # Visualisation des non-conformités de manière claire
    st.header('Non-conformités')
    non_conformities = [req for req in checklist if req.get("score") in ["C", "D", "MAJOR", "KO"]]
    
    if non_conformities:
        st.write(f"Nombre de non-conformités: {len(non_conformities)}")
        comments_to_save = {}
        for nc in non_conformities:
            with st.expander(f"Non-conformité {nc.get('requirementUuid')}"):
                st.write(f"Score: {nc.get('score')}")
                st.write(f"Explication: {nc.get('explanationText', 'Non disponible')}")
                st.json(nc)  # Afficher tous les détails de la non-conformité
                # Ajouter un commentaire pour la non-conformité
                comment = st.text_area(f"Ajouter un commentaire pour la requirement {nc.get('requirementUuid')}", key=f"nc_{nc.get('requirementUuid')}")
                comments_to_save[nc.get('requirementUuid')] = comment
        
        # Enregistrer tous les commentaires
        if st.button("Enregistrer tous les commentaires de non-conformités"):
            add_comment(comments_to_save)
            st.success("Tous les commentaires de non-conformités ont été enregistrés avec succès !")
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
