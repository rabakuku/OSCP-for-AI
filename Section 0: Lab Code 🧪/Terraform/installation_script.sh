#! /bin/bash

    #if file is there, do not run starte up script again
    FLAG_FILE="/etc/startup_was_launched"

    if [[ -f "$FLAG_FILE" ]]; then
    echo "Startup script already ran once. Exiting."
    exit 0
    fi    

echo "✅ Installation of Ollama"
wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/prepare_lab_env.sh"
    echo "✅ Installation of Streamlit"
    # Make executable and run
    chmod +x prepare_lab_env.sh
    ./prepare_lab_env.sh
    echo "✅ Installation of Ollama is Complete!"


echo "✅ Installation of LLMS"
wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/llms.sh"
    echo "✅ Installation of Streamlit"
    # Make executable and run
    chmod +x llms.sh
    ./llms.sh
    echo "✅ Installation of LLMS is Complete!"


echo "✅ Installation of OSCP-for-AI Lab Environment Setup + Streamlit App"
wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/lab_streamlit_app_setup.sh"
 wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/requirements.txt"
# Make executable and run
    chmod +x lab_streamlit_app_setup.sh
    ./lab_streamlit_app_setup.sh
    echo "✅ Installation of OSCP-for-AI Lab Environment Setup + Streamlit App is Complete!"
echo "=========================================="
echo "Setup Complete!"
echo ""
echo "To start the lab run:"
echo "source $VENV_NAME/bin/activate"
echo "streamlit run home.py"
echo "=========================================="



echo "✅ Installation of OSCP-for-AI Lab Environment Setup + Streamlit App"
wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/lab_streamlit_app_setup.sh"
 wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/requirements.txt"
# Make executable and run
    chmod +x lab_streamlit_app_setup.sh
    ./lab_streamlit_app_setup.sh
    echo "✅ Installation of OSCP-for-AI Lab Environment Setup + Streamlit App is Complete!"
echo "=========================================="
echo "Setup Complete!"
echo ""
echo "To start the lab run:"
echo "source $VENV_NAME/bin/activate"
echo "streamlit run home.py"
echo "=========================================="


echo "✅ Installation of Garak + Conda"
wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/garak_sh"
# Make executable and run
    chmod +x garak_sh
    ./garak_sh
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
wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/giskard_PyRIT.sh"
# Make executable and run
    chmod +x giskard_PyRIT.sh
    ./giskard_PyRIT.sh
    echo "✅ Installation of Giskard + PyRIT is Complete!"

   
