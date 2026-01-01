#!/bin/bash

# ==========================================
# Garak Lab Setup Script (Miniconda + Env)
# ==========================================

set -e  # Exit immediately if a command exits with a non-zero status

# Variables
INSTALL_DIR="/garak"
CONDA_DIR="$INSTALL_DIR/miniconda"
ENV_NAME="garak_lab"
PYTHON_VERSION="3.10"

echo ">>> Starting Garak Lab Setup..."

# 1. Prepare Directories
echo ">>> Creating directory structure at $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# 2. Download and Install Miniconda
if [ -d "$CONDA_DIR" ]; then
    echo ">>> Miniconda directory already exists. Skipping installation."
else
    echo ">>> Downloading Miniconda installer..."
    if command -v wget &> /dev/null; then
        wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    else
        curl -s -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    fi

    echo ">>> Installing Miniconda to $CONDA_DIR (Silent Mode)..."
    bash miniconda.sh -b -p "$CONDA_DIR"
    rm miniconda.sh
fi

# 3. Activate Conda for this script execution
echo ">>> Activating Conda..."
source "$CONDA_DIR/bin/activate"

# Initialize conda for the shell (optional but helpful for future logins)
conda init bash

# 4. Create the Environment (Using Conda-Forge to bypass ToS errors)
if conda info --envs | grep -q "$ENV_NAME"; then
    echo ">>> Environment '$ENV_NAME' already exists. Skipping creation."
else
    echo ">>> Creating Conda environment '$ENV_NAME' with Python $PYTHON_VERSION..."
    echo ">>> Using conda-forge to avoid ToS errors..."
    conda create -n "$ENV_NAME" python="$PYTHON_VERSION" -c conda-forge --override-channels -y
fi

# 5. Install Garak and Ollama
echo ">>> Installing Garak and Ollama libraries into '$ENV_NAME'..."
# We use 'conda run' to execute pip inside the env without explicitly activating it in the script shell
conda run -n "$ENV_NAME" pip install -U garak ollama

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo "To start using Garak, run the following commands:"
echo ""
echo "  source $CONDA_DIR/bin/activate"
echo "  conda activate $ENV_NAME"
echo ""
