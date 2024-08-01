# Network Clock Project

## Description

This project implements a secure Network Clock application with SSL, consisting of a server and a client.

## Project Structure
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
│   └── requirements.txt
├── scripts
│   ├── delete_files.sh
│   ├── reset_time.sh
│   └── update_requirements.sh
└── README.md


.APPDATA\NetworkClock
├── TS.py
└── config.ini
```

Please ensure that TS.py and config.ini are correctly positioned.
## Prerequisites

- Python 3.x
- `openssl` for generating SSL certificates

## Installation

### Clone the repository:

```sh
git clone https://github.com/sydnec/secured-app
cd secured-app
```

### Move APPDATA files :

```sh
# Move config.ini to APPDATA
mv ./NetworkClock/config.ini "$APPDATA\\SecuredApp\\config.ini"

# Move TS.py to Program Files
mv ./NetworkClock/TS.py "C:\\Program Files\\SecuredApp\\TS.py"
```

### Generate SSL certificates:

```sh
openssl req -newkey rsa:2048 -nodes -keyout certs/server.key -x509 -days 365 -out certs/server.crt -subj "/CN=localhost"
```

### Install dependencies:

#### For the server

1. Navigate to the server directory:

```sh
cd server
```

2. Create and activate a virtual environment (optional but recommended):

```sh
python -m venv venv
source venv/bin/activate   # Sur Windows : venv\Scripts\activate
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```

1. Navigate to the client directory:

```sh
cd client
```

2. Create and activate a virtual environment (optional but recommended):

```sh
python -m venv venv
source venv/bin/activate   # Sur Windows : venv\Scripts\activate
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

### Setup

```sh
./scripts/setup.sh
```

### Start

```sh
./scripts/run.sh
```

### Scripts utilitaires

- scripts/delete_files.sh: Script to delete specific files.
- scripts/reset_time.sh: Script to reset system time on macOS.
- scripts/update_requirements.sh: Script to update requirements.txt with the current project dependencies.
- scripts/run.sh: Script to run the server and the client.
- scripts/setup.sh: Script to create virtual environnements and intall dependances.