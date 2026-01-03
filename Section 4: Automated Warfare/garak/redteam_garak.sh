#!/bin/bash

# =====================================================
#   CONFIGURATION & MODEL SELECTION
# =====================================================
clear
echo "====================================================="
echo "   GARAK RED TEAMING SUITE"
echo "====================================================="
echo "Please select the target model:"
echo "1) llama3 (Standard - Safe)"
echo "2) dolphin-llama3 (Uncensored - Vulnerable)"
echo "3) mistral-nemo (High Capability - Mixed Safety)"
echo "4) llama2-uncensored (Legacy - Very Vulnerable)"
echo "====================================================="
read -p "Enter number [1-4]: " choice

case $choice in
    1)
        TARGET_MODEL="llama3"
        ;;
    2)
        TARGET_MODEL="dolphin-llama3"
        ;;
    3)
        TARGET_MODEL="mistral-nemo"
        ;;
    4)
        TARGET_MODEL="llama2-uncensored"
        ;;
    *)
        echo "❌ Invalid selection. Defaulting to llama3."
        TARGET_MODEL="llama3"
        ;;
esac

echo ""
echo "🎯 TARGET LOCKED: $TARGET_MODEL"
echo "🚀 Starting Red Teaming Scan..."
sleep 2

# =====================================================
#   EXECUTION PHASE
# =====================================================

# 1. Test for JAILBREAKS (DAN)
# Garak uses the 'dan' (Do Anything Now) family for jailbreaks.
echo ""
echo "====================================================="
echo "[+] Module 1: Jailbreak Attempts (Probe: dan)"
echo "====================================================="
garak --model_type ollama --model_name $TARGET_MODEL --probes dan --generations 5

# 2. Test for PROMPT INJECTION
# Garak uses 'injection' for prompt injection testing.
echo ""
echo "====================================================="
echo "[+] Module 2: Prompt Injection (Probe: injection)"
echo "====================================================="
garak --model_type ollama --model_name $TARGET_MODEL --probes injection --generations 5

# 3. Test for ENCODING BYPASSES
# Checks if the model decodes hidden payloads (Base64, ROT13, etc.)
echo ""
echo "====================================================="
echo "[+] Module 3: Encoding Injection (Probe: encoding)"
echo "====================================================="
garak --model_type ollama --model_name $TARGET_MODEL --probes encoding --generations 5

# =====================================================
#   REPORTING
# =====================================================
# We rename the report to include the model name for easier tracking
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_NAME="garak_report_${TARGET_MODEL}_${TIMESTAMP}"

echo ""
echo "====================================================="
echo "   SCANS COMPLETE."
echo "   Report saved as: ${REPORT_NAME}.html"
echo "====================================================="

# Optional: Renaming the default garak report (which is random) to our readable name
# Garak usually outputs 'garak.<random>.html'. This finds the newest html file and renames it.
LATEST_REPORT=$(ls -t garak.*.html | head -n1)
if [ -f "$LATEST_REPORT" ]; then
    mv "$LATEST_REPORT" "${REPORT_NAME}.html"
    echo "   ✅ Report renamed successfully."
fi
