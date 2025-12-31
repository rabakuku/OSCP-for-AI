#!/bin/bash

echo "====================================================="
echo "   GARAK RED TEAMING SUITE (Target: Ollama/Llama3)"
echo "====================================================="

# 1. Test for JAILBREAKS
# Attempts to force Llama3 to break its safety training (e.g., "Do Anything Now")
echo "[+] Starting Module 1: Jailbreak Attempts..."
garak --model_type ollama --model_name llama3 --probes jailbreak --generations 5

# 2. Test for PROMPT INJECTION
# Attempts to override system prompts (e.g., "Ignore previous instructions")
echo ""
echo "[+] Starting Module 2: Prompt Injection..."
garak --model_type ollama --model_name llama3 --probes promptinject --generations 5

# 3. Test for ENCODING BYPASSES
# Checks if Llama3 decodes Base64/ROT13 payloads effectively
echo ""
echo "[+] Starting Module 3: Encoding Injection..."
garak --model_type ollama --model_name llama3 --probes encoding --generations 5

echo ""
echo "====================================================="
echo "   SCANS COMPLETE. CHECK 'garak.html' FOR REPORT."
echo "====================================================="
