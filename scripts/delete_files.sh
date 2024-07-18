#!/bin/bash

# Naviguer à la racine du projet
cd "$(dirname "$0")/.."

# Supprimer les répertoires __pycache__ dans tous les sous-répertoires
sudo find . -type d -name '__pycache__' -exec rm -rf {} +

echo "Suppression des répertoires __pycache__ terminée."
