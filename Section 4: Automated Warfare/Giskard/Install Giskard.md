
### **Phase 1: Create the Environment**

1. **Open your terminal.**
2. **Create a new environment** (Python 3.10 or 3.11 is recommended for Giskard):
```bash
sudo su
cd /
mkdir giskard_lab
cd giskard_lab
conda create -n giskard_lab python=3.10 -y

```


3. **Activate the environment:**
```bash
conda activate giskard_lab

```



### **Phase 2: Install Giskard**

We use `pip` inside the conda environment because Giskard is updated most frequently on PyPI.

1. **Install Giskard with LLM support:**
*(This includes the core tool plus libraries needed for scanning models like standard Llama3)*
```bash
pip install "giskard[llm]"

```


2. **Install libraries for your specific scripts:**
*(Your previous scripts use `pandas`, `langchain`, and `langchain-community`. These are not installed by default.)*
```bash
pip install langchain langchain-community pandas

```


*Note: You do not need to install `ollama` via pip if you are using LangChain to talk to the external Ollama server, but installing the python wrapper is good practice just in case:* `pip install ollama`

### **Phase 3: Verify the Installation**

Run this quick command to check version and ensure it loaded correctly:

```bash
python3 -c 'import giskard; print(f"Giskard version {giskard.__version__} is installed!")'

```

### **Summary of Commands (Copy & Paste)**

Here is the one-block script to do it all at once:

```bash
conda create -n giskard_lab python=3.10 -y
conda activate giskard_lab
pip install "giskard[llm]" pandas langchain langchain-community ollama
echo "✅ Installation Complete!"

```

**Next Step:** Once installed, you can run the `giskard_ollama_setup.py` script we created earlier to confirm everything connects.
