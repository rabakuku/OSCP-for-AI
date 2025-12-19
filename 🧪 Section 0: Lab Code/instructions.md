Here is the Markdown file containing the instructions on how to run the setup, including diagrams of the file structure before and after execution.

You can save this as `HOW_TO_RUN.md` in your project directory.

---

```markdown
# 🚀 OSCP-for-AI Lab Environment Setup Guide

This guide details how to use the provided `setup.sh` script to automatically download the required lab code from GitHub, restructure it, and install all necessary Python dependencies.

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

Once the script completes successfully, it will have downloaded the lab files, moved them to the root, and created the virtual environment.

```text
your_project_root/ 📂
│
├── venv/             📂 (Python virtual environment created by script)
│   └── ...
├── pages/            📂 (Downloaded Lab Pages directory)
│   ├── 1_Introduction.py
│   └── ...
├── .env              📄 (Optional: Create this yourself for API keys)
├── home.py           📄 (Downloaded main application entry point)
├── requirements.txt  📄
├── setup.sh          📄
└── utils.py          📄 (Downloaded utility functions)

```

---

## 🏃‍♂️ How to Run the Setup

Follow these steps in your Linux terminal (or WSL on Windows/Terminal on macOS) to prepare your environment.

### Step 1: Prepare the Directory

Create a new, empty folder for your lab and navigate into it.

```bash
mkdir ai_security_lab
cd ai_security_lab

```

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
streamlit run home.py

```

The terminal will output a local URL (usually `http://localhost:8501`). Open that link in your browser to access the labs.

---

**🎉 Happy Hacking!**

```

```
