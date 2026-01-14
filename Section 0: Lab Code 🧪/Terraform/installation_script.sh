#! /bin/bash

    #if file is there, do not run starte up script again
    FLAG_FILE="/etc/startup_was_launched"

    if [[ -f "$FLAG_FILE" ]]; then
    echo "Startup script already ran once. Exiting."
    exit 0
    fi    
  # 2. Prepare the Lab Environment
    # ------------------------------
    echo "Setting up Course Files..."
    mkdir -p /oscp-for-ai
    mkdir -p /lab-installation-error
    mkdir -p /lab-scripts
    
# Define the list of directories to check
DIRS=("/oscp-for-ai" "/lab-installation-error" "/lab-scripts")

# Loop through each directory in the array
for dir in "${DIRS[@]}"; do
    # Check if the directory does NOT exist
    if [ ! -d "$dir" ]; then
        echo "Creating directory: $dir"
        # Using -p to handle parent directory creation safely
        sudo mkdir -p "$dir"
    else
        echo "Directory already exists: $dir"
    fi
done
    
echo "✅ Installation of Ollama"
wget -P /lab-scripts "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/prepare_lab_env.sh"
    echo "✅ Installation of Streamlit"
    # Make executable and run
    chmod +x /lab-scripts/prepare_lab_env.sh
    bash /lab-scripts/prepare_lab_env.sh > /lab-installation-error/prepare_lab_env.log 2>&1
    echo "✅ Installation of Ollama is Complete!"


echo "✅ Installation of LLMS"
wget -P /lab-scripts "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/llms.sh"
    echo "✅ Installation of Streamlit"
    # Make executable and run
    chmod +x /lab-scripts/llms.sh
    bash /lab-scripts/llms.sh > /lab-installation-error/llms.log 2>&1
    echo "✅ Installation of LLMS is Complete!"


echo "✅ Installation of OSCP-for-AI Lab Environment Setup + Streamlit App"
wget -P /lab-scripts "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/lab_streamlit_app_setup.sh"
 wget -P /lab-scripts "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/requirements.txt"
# Make executable and run
    chmod +x /lab-scripts/lab_streamlit_app_setup.sh
    bash /lab-scripts/lab_streamlit_app_setup.sh > /lab-installation-error/lab_streamlit_app_setup.log 2>&1
    echo "✅ Installation of OSCP-for-AI Lab Environment Setup + Streamlit App is Complete!"
echo "=========================================="
echo "Setup Complete!"
echo ""
echo "To start the lab run:"
echo "source $VENV_NAME/bin/activate"
echo "streamlit run home.py"
echo "=========================================="



echo "✅ Installation of Garak + Conda"
wget -P /lab-scripts "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/garak.sh"
# Make executable and run
    chmod +x /lab-scripts/garak.sh
    bash  /lab-scripts/garak.sh > /lab-installation-error/garak.log 2>&1
    echo "✅ Installation of Garak + Conda is Complete!"
echo "=========================================="
echo "✅ Installation of garak is Complete!"
echo "=========================================="
echo "To start using Garak, run the following commands:"
echo ""
echo "  source $CONDA_DIR/bin/activate"
echo "  conda activate $ENV_NAME"
echo ""



echo "✅ Installation of Giskard + PyRIT!"
wget -P /lab-scripts "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/giskard_PyRIT.sh"
# Make executable and run
    chmod +x /lab-scripts/giskard_PyRIT.sh
    bash /lab-scripts/giskard_PyRIT.sh > /lab-installation-error/giskard_PyRIT.log 2>&1
    echo "✅ Installation of Giskard + PyRIT is Complete!"

   
