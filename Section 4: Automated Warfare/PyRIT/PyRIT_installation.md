---

### **PyRIT Installation & Configuration Steps**

#### **1. Environment Setup (Conda)**

First, create a dedicated space for PyRIT to prevent version conflicts with your Giskard lab.

```bash
sudo su
cd /
conda --h
conda env list
mkdir PyRIT_lab
conda create -n PyRIT_lab python=3.11 -y
conda activate PyRIT_lab
pip install pandas python-dotenv pyrit

```
---


