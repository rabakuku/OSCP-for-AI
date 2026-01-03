Installing **PyRIT** (Python Risk Identification Tool) within a Conda environment is the recommended approach to avoid dependency conflicts and ensure you are using a compatible Python version. Microsoft officially recommends **Python 3.10, 3.11, or 3.12** for PyRIT.

---

### **Step-by-Step Installation Guide**

#### **1. Create the Conda Environment**

Open your terminal (or Anaconda Prompt) and create a new environment. It is best to specify Python 3.11, as it is widely tested for PyRIT stability.

```bash
conda create -n pyrit-env python=3.11 -y

```

#### **2. Activate the Environment**

Once created, switch into the new environment so that all subsequent installations are isolated.

```bash
conda activate pyrit-env

```

#### **3. Install PyRIT via Pip**

PyRIT is primarily distributed as a Python library. Even within Conda, you use `pip` to pull the package from the Python Package Index (PyPI).

```bash
pip install pyrit

```

#### **4. (Optional) Install from GitHub for Latest Features**

If you want the cutting-edge features that aren't yet in the stable PyPI release, you can install directly from the source code.

```bash
git clone https://github.com/Azure/PyRIT.git
cd PyRIT
pip install .

```

#### **5. Verify the Installation**

To confirm that PyRIT is installed correctly, you can try to import it in a Python shell:

```python
python -c "import pyrit; print('PyRIT version:', pyrit.__version__ if hasattr(pyrit, '__version__') else 'Installed')"

```

---

### **Why Use Conda for PyRIT?**

* **Python Version Control:** PyRIT strictly requires Python **3.10 to 3.13** (it does not support 3.9 or older). Conda makes it easy to pin this specific version.
* **Isolated Workspace:** PyRIT installs many heavy dependencies (like `openai`, `langchain`, and `playwright`). Conda ensures these don't break your other projects.
* **Cross-Platform:** Since you have an interest in Linux configuration, Conda provides a consistent experience whether you are on Ubuntu or WSL.

---

### **Important: Browser Dependencies**

PyRIT uses **Playwright** for some of its web-based targets. After installing PyRIT, you may need to install the browser binaries:

```bash
playwright install

```

Would you like me to help you configure your **`.env`** file to connect PyRIT to your local **Ollama** instance for red teaming?
