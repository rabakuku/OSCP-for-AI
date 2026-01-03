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


Yes, **Promptfoo has a comprehensive web GUI** known as the **Web Viewer**.

While Promptfoo is primarily a CLI-driven tool, the web interface is the primary way developers visualize and analyze their results. It transforms raw terminal data into a structured, interactive dashboard.

### **How to Access It**

After running an evaluation with `promptfoo eval`, you can launch the GUI by running:

```bash
promptfoo view

```

This starts a local web server (usually at `http://localhost:3000`) and opens the dashboard in your default browser.

### **Key Features of the Web GUI**

1. **Side-by-Side Comparison Matrix:**
The core of the UI is a grid where columns represent different models (Ollama, GPT-4, etc.) and rows represent your test cases. This allows you to see exactly how different models responded to the same prompt at a glance.
2. **Visual Assertions (Pass/Fail):**
Each cell is color-coded. **Green** means your safety or quality assertions passed, and **Red** means they failed. You can click any cell to see the full raw input, output, and the "rationale" behind the grade.
3. **Performance Metrics:**
The UI displays detailed stats for every run, including:
* **Latency:** How many milliseconds the model took to respond.
* **Cost:** Calculated based on token usage (for API providers).
* **Token Usage:** Breakdown of prompt vs. completion tokens.


4. **Eval History:**
A sidebar allows you to browse every evaluation you have ever run on that machine, making it easy to track whether your model’s security or quality is improving over time.
5. **Interactive "Eval Creator":**
There is a "New Eval" button that lets you draft prompts and test cases directly in the UI without touching your `yaml` file. You can run these tests live and save the configuration when you're happy with it.
6. **Tracing (OpenTelemetry):**
If you use complex RAG (Retrieval-Augmented Generation) pipelines, the UI can show traces, visualizing every step the AI took—from searching the database to generating the final answer.

### **Deployment Options**

* **Local:** Runs on your laptop (the most common use case).
* **Self-Hosted:** You can run Promptfoo in a **Docker container** to host a shared dashboard for your entire team.
* **Cloud (promptfoo.app):** You can use the `promptfoo share` command to upload your results to a private, shareable URL for collaboration.

