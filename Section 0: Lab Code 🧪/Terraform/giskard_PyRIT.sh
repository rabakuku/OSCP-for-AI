#! /bin/bash
#install and setup Giskard
cd /
mkdir giskard_lab
cd giskard_lab
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda create -n giskard_lab python=3.10 -y
conda activate giskard_lab
pip install "giskard[llm]" -y 
pip install langchain langchain-community pandas langchain-ollama -y 


  #install and setup PyRIT
cd / 
mkdir PyRIT_lab
conda create -n PyRIT_lab python=3.11 -y
conda activate PyRIT_lab
cd PyRIT_lab
pip install pandas python-dotenv pyrit tabulate -y
wget https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%204%3A%20Automated%20Warfare/PyRIT/pyrit_master.py
