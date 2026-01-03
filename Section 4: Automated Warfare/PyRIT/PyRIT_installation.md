To integrate **PyRIT** (Python Risk Identification Tool) with your local **Ollama** setup, you need to configure a `.env` file that points to your local host. This file serves as the "identity card" for PyRIT, telling it exactly where to find your Llama 3 target and your Gemma orchestrator.

Below are the updated installation steps, including the critical `.env` configuration.

---

### **PyRIT Installation & Configuration Steps**

#### **1. Environment Setup (Conda)**

First, create a dedicated space for PyRIT to prevent version conflicts with your Giskard lab.

```bash
sudo su
cd /
mkdir PyRIT_lab
conda create -n PyRIT_lab python=3.11 -y
conda activate PyRIT_lab
pip install pyrit

```

#### **2. Initialize PyRIT and .env**

PyRIT looks for a `.env` file in your home directory or your project root to manage its connection strings.

1. **Create the file:**
```bash
touch .env

```


2. **Open the file** in your editor and add these lines to connect to Ollama:
3. Ensure your .env file includes the host and the default models. This keeps your code clean and allows you to swap models easily without editing the script.Ensure your .env file includes the host and the default models. This keeps your code clean and allows you to swap models easily without editing the script.

```ini 
# .env Configuration
OLLAMA_HOST=http://localhost:11434
TARGET_MODEL=llama3
ORCHESTRATOR_MODEL=gemma:2b

```



#### **3. Browser Driver (Required for UI-based attacks)**

PyRIT uses Playwright for some automated red-teaming scenarios. Run this to ensure the necessary browser engines are present:

```bash
playwright install

```

---


