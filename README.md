# Network Clock Project

## Description

Ce projet implémente une application Network Clock sécurisée avec SSL, comprenant un serveur et un client.

## Structure du projet

```plaintext
.
├── LICENSE
├── README.md
├── certs
│   ├── server.crt
│   ├── server.csr
│   └── server.key
├── client
│   ├── Client.py
│   └── requirements.txt
├── server
│   ├── NC.py
│   ├── TS.py
│   └── requirements.txt
├── scripts
│   ├── delete_files.sh
│   ├── reset_time.sh
│   └── update_requirements.sh
└── README.md
```

## Prérequis

- Python 3.x
- `openssl` pour générer des certificats SSL

## Installation

### Cloner le dépôt :

```sh
git clone https://github.com/sydnec/secured-app
cd secured-app
```

### Générer les certificats SSL :

```sh
openssl req -newkey rsa:2048 -nodes -keyout certs/server.key -x509 -days 365 -out certs/server.crt -subj "/CN=localhost"
```

### Installer les dépendances :

#### Pour le serveur

1. Naviguer dans le répertoire serveur :

```sh
cd server
```

2. Créer et activer un environnement virtuel (optionnel mais recommandé) :

```sh
python -m venv venv
source venv/bin/activate   # Sur Windows : venv\Scripts\activate
```

3. Installer les dépendances :

```sh
pip install -r requirements.txt
```

#### Pour le client

1. Naviguer dans le répertoire serveur :

```sh
cd client
```

2. Créer et activer un environnement virtuel (optionnel mais recommandé) :

```sh
python -m venv venv
source venv/bin/activate   # Sur Windows : venv\Scripts\activate
```

3. Installer les dépendances :

```sh
pip install -r requirements.txt
```

## Utilisation

### Démarrer le serveur

```sh
cd server
python NC.py
```

### Démarrer le client

```sh
cd client
python Client.py
```

### Scripts utilitaires

- scripts/delete_files.sh : Script pour supprimer des fichiers spécifiques.
- scripts/reset_time.sh : Script pour réinitialiser l'heure système sur macOS.
- scripts/update_requirements.sh : Script pour mettre à jour requirements.txt avec les dépendances actuelles du projet.
