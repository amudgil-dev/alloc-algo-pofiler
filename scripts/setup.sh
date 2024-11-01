#!/bin/bash

# code to update apt - the package manager
# sudo apt update

# installing python tools
# sudo apt install python3.12-venv


# Create a new virtual environment
python3 -m venv venv

echo " - Created venv"

# Activate the virtual environment
source venv/bin/activate

echo " - Activated venv"

# Upgrade pip
pip install --upgrade pip

echo " - Upgraded pip"

# Install dependencies
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please create one with your project dependencies."
    exit 1
fi

echo " - Installed dependencies from requirements.txt"

echo "Virtual environment created and dependencies installed."

# Create s_run.sh script

# cat > s_run.sh << EOL
# #!/bin/bash

# # Activate the virtual environment
source venv/bin/activate
echo "Activated the virtual environment."
