import os

# Définir les chemins des répertoires
repertoire_source = r"E:\Python\MLTVA2"
fichier_sortie = r"E:\Python\MLTVA2\Infos\mltva.txt"

def generer_arborescence(repertoire, niveau=0):
    """
    Génère une représentation en arborescence d'un répertoire.
    :param repertoire: Chemin du répertoire à parcourir.
    :param niveau: Niveau de profondeur dans l'arborescence (pour indentation).
    :return: Une chaîne de caractères représentant l'arborescence.
    """
    arborescence = ""
    try:
        # Lister le contenu du répertoire
        elements = os.listdir(repertoire)
        for i, element in enumerate(sorted(elements)):
            chemin_element = os.path.join(repertoire, element)
            
            # Ignorer les répertoires .git et __pycache__
            if element in [".git", "__pycache__","fichiers_ui_qt"]:
                continue
            
            # Ajouter un préfixe pour indiquer la position dans l'arborescence
            prefixe = "└── " if i == len(elements) - 1 else "├── "
            arborescence += "    " * niveau + prefixe + element + "\n"
            
            # Si c'est un répertoire, appeler récursivement la fonction
            if os.path.isdir(chemin_element):
                arborescence += generer_arborescence(chemin_element, niveau + 1)
    except PermissionError:
        arborescence += "    " * niveau + "└── (accès refusé)\n"
    return arborescence

# Ouvrir le fichier de sortie en mode écriture
with open(fichier_sortie, "w", encoding="utf-8") as f:
    # Ajouter l'en-tête avec l'arborescence
    f.write("==== Arborescence du projet ====\n")
    f.write(f"Répertoire source: {repertoire_source}\n\n")
    f.write(generer_arborescence(repertoire_source))
    f.write("\n" + "=" * 80 + "\n\n")

    # Parcourir le répertoire source et ses sous-répertoires
    for repertoire_actuel, sous_repertoires, fichiers in os.walk(repertoire_source):
        # Exclure les répertoires .git et __pycache__
        sous_repertoires[:] = [d for d in sous_repertoires if d not in [".git", "__pycache__","fichiers_ui_qt"]]
        
        for fichier in fichiers:
            # Vérifier si le fichier a l'extension .py
            if fichier.endswith(".py"):
                # Construire le chemin complet du fichier
                chemin_complet = os.path.join(repertoire_actuel, fichier)
                
                # Écrire le chemin complet et le nom du fichier dans le fichier de sortie
                f.write(f"Chemin: {chemin_complet}\n")
                f.write(f"Fichier: {fichier}\n")
                f.write("Contenu:\n")
                
                try:
                    # Lire le contenu du fichier .py
                    with open(chemin_complet, "r", encoding="utf-8") as fichier_py:
                        contenu = fichier_py.read()
                        f.write(contenu)
                except Exception as e:
                    # Gérer les erreurs éventuelles (par exemple, encodage incorrect)
                    f.write(f"Erreur lors de la lecture du fichier : {e}\n")
                
                # Ajouter un séparateur pour une meilleure lisibilité
                f.write("\n" + "=" * 80 + "\n\n")

print(f"La liste des fichiers .py et leur contenu ont été sauvegardés dans {fichier_sortie}")