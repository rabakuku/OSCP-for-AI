#!/bin/bash

# ================================================
# OSCP-for-AI Lab Setup Script
# ================================================
# This script downloads specific lab code from the repository,
# creates a Python virtual environment, and installs dependencies.

# Exit immediately if a command exits with a non-zero status
set -e

# Define Variables
REPO_URL="https://github.com/rabakuku/OSCP-for-AI.git"
# The specific, complex folder name on GitHub
GITHUB_SOURCE_FOLDER="🧪 Section 0: Lab Code"
VENV_NAME="venv"

echo "=========================================="
echo "Starting OSCP-for-AI Lab Environment Setup"
echo "=========================================="

# --- Step 1: Sparse Checkout of lab code ---
echo "[1/4] Initializing Git and performing sparse checkout..."

# Initialize a new git repo here temporarily
if [ -d ".git" ]; then
    echo "Git repository already exists here. Skipping init."
else
    git init
    git remote add -f origin "$REPO_URL"
fi

# Enable sparse-checkout to only get the folder we want
git config core.sparseCheckout true

# Write the specific folder path to the sparse-checkout config
# We use quotes to handle spaces and emojis
echo "$GITHUB_SOURCE_FOLDER" > .git/info/sparse-checkout

# Pull the main branch (this will only download the defined folder)
echo "Pulling lab code from remote..."
git pull origin main

# --- Step 2: Restructure Files ---
echo "[2/4] Restructuring files to project root..."

# Check if the source folder exists after the pull
if [ -d "$GITHUB_SOURCE_FOLDER" ]; then
    # Move contents of the downloaded folder to the current directory root
    # Use find to handle hidden files correctly, exclude the folder itself
    find "$GITHUB_SOURCE_FOLDER" -mindepth 1 -maxdepth 1 -exec mv -t . {} +

    # Remove the now empty source folder
    rmdir "$GITHUB_SOURCE_FOLDER"
    # Remove the temporary git directory to detach from the remote repo
    rm -rf .git
    echo "Files restructured successfully. Directory is detached from Git."
else
    echo "Error: The expected source folder was not downloaded. Check the repository structure."
    exit 1
fi


# --- Step 3: Create Virtual Environment ---
echo "[3/4] Setting up Python virtual environment..."

if [ -d "$VENV_NAME" ]; then
    echo "Virtual environment '$VENV_NAME' already exists."
else
    python3 -m venv "$VENV_NAME"
    echo "Created virtual environment: $VENV_NAME"
fi


# --- Step 4: Install Dependencies ---
echo "[4/4] Installing Python dependencies..."

# Activate environment and install
source "$VENV_NAME"/bin/activate

# Upgrade pip first
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependencies installed successfully."
else
    echo "Warning: requirements.txt not found. Skipping dependency installation."
fi

echo "=========================================="
echo "Setup Complete!"
echo ""
echo "To start the lab run:"
echo "source $VENV_NAME/bin/activate"
echo "streamlit run home.py"
echo "=========================================="
