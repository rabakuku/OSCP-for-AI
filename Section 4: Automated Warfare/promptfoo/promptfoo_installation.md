We are looking at **Promptfoo**. Unlike the previous tools, Promptfoo is primarily a **Node.js-based** framework, but it is extremely popular in the Python community because it allows you to test Python-based LLM applications and provides a beautiful, shareable web UI.

### **1. Installation Steps (Conda + Node.js)**

Since Promptfoo is a Node.js tool, we will use Conda to manage the Node.js environment so it stays isolated from your system.

1. **Create and Activate the Environment:**
```bash
conda create -n promptfoo-env nodejs=20 -y
conda activate promptfoo-env

```


2. **Install Promptfoo Globally (in the environment):**
```bash
npm install -g promptfoo

```


3. **Verify:**
```bash
promptfoo --version

```

---
