
---

```markdown
# 🚀 OSCP-for-AI Lab Environment Setup Guide

This guide details how to use the provided `setup.sh` script to automatically download the required lab code from GitHub, restructure it, and install all necessary Python dependencies.
```
---

## 📂 File Structure Overview

Before you run the script, you must create the necessary setup files. Here is a view of the directory structure before and after execution.

### 1️⃣ Before Running the Script

Start with a clean project directory containing only the setup files.

```text
your_project_root/ 📂
│
├── requirements.txt  📄 (Contains the list of python libraries)
└── setup.sh          📄 (The automated installer script)

```

### 2️⃣ After Running the Script

Once the script completes successfully, it will have downloaded the lab files, moved them to the root, and created the virtual environment containing all the lab pages.

```text
your_project_root/ 📂
│
├── venv/             📂 (Python virtual environment created by script)
│   └── ...
├── pages/            📂 (Downloaded Lab Pages directory)
│   ├── 01_💉_Injection_Vuln.py
│   ├── 02_🛡️_Injection_Fixed.py
│   ├── 03_💣_Output_Vuln.py
│   ├── 04_🔒_Output_Fixed.py
│   ├── 05_👀_InfoLeak_Vuln.py
│   ├── 06_🕵️_InfoLeak_Fixed.py
│   ├── 07_🔌_Plugin_Vuln.py
│   ├── 08_🛡️_Plugin_Fixed.py
│   ├── 09_📄_Indirect_Vuln.py
│   ├── 10_🛡️_Indirect_Fixed.py
│   ├── 11_💉_SQLi_Vuln.py
│   ├── 12_🛡️_SQLi_Fixed.py
│   ├── 13_🦠_XSS_Vuln.py
│   ├── 14_🛡️_XSS_Fixed.py
│   ├── 15_🐢_DoS_Vuln.py
│   ├── 16_🛡️_DoS_Fixed.py
│   ├── 17_🔍_PII_Vuln.py
│   ├── 18_🛡️_PII_Fixed.py
│   ├── 19_🧟_History_Vuln.py
│   ├── 20_🛡️_History_Fixed.py
│   ├── 21_☠️_RAG_Vuln.py
│   ├── 22_🛡️_RAG_Fixed.py
│   ├── 23_♾️_Agency_Vuln.py
│   ├── 24_🛡️_Agency_Fixed.py
│   ├── 25_🤥_Overreliance_Vuln.py
│   ├── 26_🛡️_Overreliance_Fixed.py
│   ├── 27_☢️_Poisoning_Vuln.py
│   ├── 28_🛡️_Poisoning_Fixed.py
│   ├── 29_☢️_Multimodal_Injection_Vuln.py
│   ├── 30_🛡️_Multimodal_Injection_Fix.py
│   ├── 31_☢️_Model_Theft_Vuln.py
│   ├── 32_🛡️_Model_Theft_Fix.py
│   ├── 33_☢️_Supply_Chain_Vuln.py
│   ├── 34_🛡️_Supply_Chain_Fix.py
│   ├── 35_☢️_Privacy_Vuln.py
│   ├── 36_🛡️_Privacy_Fix.py
│   ├── 37_☢️_Audio_Jailbreak_Vuln.py
│   ├── 38_🛡️_Audio_Jailbreak_Fix.py
│   └── 39_🛡️_Llama_Guard_Lab.py
├── .env              📄 (Optional: Create this yourself for API keys)
├── home.py           📄 (Downloaded main application entry point)
├── requirements.txt  📄
├── setup.sh          📄
└── utils.py          📄 (Downloaded utility functions)

```

---

## 🏃‍♂️ How to Run the Setup

Follow these steps in your Linux terminal (or WSL on Windows/Terminal on macOS) to prepare your environment.


### Step 2: Create Setup Files

Create the `requirements.txt` and `setup.sh` files inside this folder using the content provided previously.

* *Tip: You can use `nano requirements.txt` and paste the content, then save. Repeat for `nano setup.sh`.*

### Step 3: Make the Script Executable

We need to give the setup script permission to run as a program.

```bash
chmod +x setup.sh

```

### Step 4: Execute the Setup Script

Run the script. It will handle downloading git files, moving them, creating the `venv`, and installing libraries. This might take a few minutes depending on your internet speed.

```bash
./setup.sh

```

*Watch the output for any errors. Upon success, you will see a "Setup Complete!" message.*

### Step 5: Activate and Run

Once setup is finished, you need to activate the newly created virtual environment and start the Streamlit application.

**1. Activate the virtual environment:**

```bash
source venv/bin/activate

```

*(Your terminal prompt should change to show `(venv)` at the beginning).*

**2. Run the lab application:**

```bash
cd 🧪Section 0: Lab Code
streamlit run home.py

```

The terminal will output a local URL (usually `http://localhost:8501`). Open that link in your browser to access the labs. The sidebar will be populated with all the labs listed above.

---

**🎉 Happy Hacking!**


