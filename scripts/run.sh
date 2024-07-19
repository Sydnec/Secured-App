#!/bin/bash

# Sortie immédiate en cas d'erreur
set -e

# Fonction pour afficher les messages d'erreur
function error_exit {
    echo "$1" >&2
    exit 1
}

# Naviguer à la racine du projet
cd "$(dirname "$0")/.." || error_exit "Impossible de naviguer à la racine du projet."

# Vérifier si les environnements virtuels existent
if [ ! -d "client/venv" ]; then
    error_exit "L'environnement virtuel pour le client n'existe pas. Veuillez créer un environnement virtuel dans client/venv avant d'exécuter ce script."
fi

if [ ! -d "server/venv" ]; then
    error_exit "L'environnement virtuel pour le serveur n'existe pas. Veuillez créer un environnement virtuel dans server/venv avant d'exécuter ce script."
fi

# Activer l'environnement virtuel du client
source client/venv/bin/activate || error_exit "Impossible d'activer l'environnement virtuel du client."

# Vérifier si le script Python du client existe
if [ ! -f "client/Client.py" ]; then
    error_exit "Le fichier client/Client.py n'existe pas."
fi

# Exécuter le script Python du client en arrière-plan
python client/Client.py &
PID_CLIENT=$!

# Désactiver l'environnement virtuel du client
deactivate

# Activer l'environnement virtuel du serveur
source server/venv/bin/activate || error_exit "Impossible d'activer l'environnement virtuel du serveur."

# Vérifier si le script Python du serveur existe
if [ ! -f "server/NC.py" ]; then
    error_exit "Le fichier server/NC.py n'existe pas."
fi

# Exécuter le script Python du serveur en arrière-plan
python server/NC.py &
PID_SERVER=$!

# Désactiver l'environnement virtuel du serveur
deactivate

# Attendre que les deux scripts se terminent
wait $PID_CLIENT
wait $PID_SERVER
