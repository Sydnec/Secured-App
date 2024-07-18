#!/bin/bash

# Fonction pour mettre à jour le fichier requirements.txt d'un répertoire spécifique
update_requirements() {
    local dir=$1
    if [ -d "$dir" ]; then
        echo "Mise à jour des dépendances dans $dir"
        source $dir/venv/bin/activate
        pip freeze > $dir/requirements.txt
        deactivate
    else
        echo "Le répertoire $dir n'existe pas."
    fi
}

# Mise à jour des dépendances pour le client
update_requirements "client"

# Mise à jour des dépendances pour le serveur
update_requirements "server"

echo "Mise à jour des requirements terminée."
