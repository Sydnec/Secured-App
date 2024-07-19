#!/bin/bash

# Function to create a virtual environment and install dependencies
setup_env() {
    local dir=$1
    echo "Setting up virtual environment for $dir"

    # Navigate to the directory
    cd $dir

    # Create virtual environment
    python3 -m venv venv

    # Activate virtual environment
    source venv/bin/activate

    # Install dependencies
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt
    else
        echo "No requirements.txt found in $dir"
    fi

    # Deactivate virtual environment
    deactivate

    # Navigate back to the root directory
    cd -
}

# Setup client environment
setup_env "client"

# Setup server environment
setup_env "server"

echo "Setup complete!"
