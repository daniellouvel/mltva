# Générer ui_main_window.py dans le répertoire ui/
pyside6-uic fichiers_ui_qt/main_window.ui -o ui/ui_main_window.py

# Générer ui_gestion_depenses.py dans le répertoire ui/
pyside6-uic fichiers_ui_qt/gestion_depenses.ui -o ui/ui_gestion_depenses.py

pyside6-uic fichiers_ui_qt/gestion_Recettes.ui -o ui/ui_gestion_Recettes.py

pyside6-uic fichiers_ui_qt/contacts_manager.ui -o ui/ui_contacts_manager.py


pyside6-uic fichiers_ui_qt/gestion_forniseur_a_regler.ui -o ui/ui_gestion_forniseur_a_regler.py




