  #! /bin/bash
    sudo systemctl daemon-reload
    sudo systemctl restart ollama
    sudo ollama pull llama3
    sudo ollama pull llama-guard3
    sudo ollama pull llava
    sudo ollama pull dolphin-llama3
    sudo ollama pull mistral-nemo
    sudo ollama pull llama2-uncensored
    sudo ollama pull gemma:2b
    sudo ollama pull phi3:mini
