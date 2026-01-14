   #! /bin/bash
  
    cd /oscp-for-ai

    # Download files (Quotes added to handle spaces and emojis in URL)
    sudo apt install git -y
    sudo apt-get install python3-venv -y
    sudo sed -i '/bullseye-backports/s/^/#/' /etc/apt/sources.list
    sudo apt update && sudo apt install -y python3-pip python3-venv git -y

 
    sudo curl -fsSL https://ollama.com/install.sh | sh
    sudo systemctl enable ollama.service
    sudo systemctl start ollama.service
    #Configure Ollama for Parallelism
    mkdir -p /etc/systemd/system/ollama.service.d
    echo "[Service]" > /etc/systemd/system/ollama.service.d/override.conf
    echo "Environment=\"OLLAMA_NUM_PARALLEL=16\"" >> /etc/systemd/system/ollama.service.d/override.conf
    echo "Environment=\"OLLAMA_MAX_LOADED_MODELS=1\"" >> /etc/systemd/system/ollama.service.d/override.conf
    echo "Environment=\"OLLAMA_KEEP_ALIVE=-1\"" >> /etc/systemd/system/ollama.service.d/override.conf
    sudo systemctl daemon-reload
    sudo systemctl restart ollama


   
