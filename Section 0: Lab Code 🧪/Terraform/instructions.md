This Markdown guide is designed to be a clear, step-by-step instruction manual for running your simplified Terraform setup. It explains how to update your variables and execute the deployment.

---

# GCP Lab Deployment Guide (One-File Variable Setup)

This repository contains a simplified Terraform configuration for deploying an AI/LLM research environment on Google Cloud Platform.

## 📋 Prerequisites

1. **Google Cloud CLI:** Installed and authenticated (`gcloud auth application-default login`).
2. **Terraform:** Version 1.0 or higher installed.

---

## 🔍 How to find your IDs via CLI

Before editing your variables, use these commands to grab the necessary IDs from your active Google Cloud account.

### 1. Get Project ID

To see your active project ID:

```bash
gcloud config get-value project

```

To list all projects you have access to:

```bash
gcloud projects list

```

### 2. Get Billing Account ID

To find the ID required for the budget alert and resource association:

```bash
gcloud billing accounts list

```

*Note: The ID will look like `01X1X1-XXXXXX-XXXXXX`.*

### 3. Get Your Public IP

To get your current IP in the format needed for the `allowed_source_ip` variable:
* Visit [WhatsMyIPAddress](https://whatismyipaddress.com/) to find your IP.*


---

## 🛠️ Setup Instructions

### 1. Update your Configuration

Open `variables.tf` and replace the `default` values with the information you gathered above.

**File: `variables.tf**`

```hcl
variable "project_id" {
  default = "YOUR_PROJECT_ID_HERE"
}

variable "billing_account_id" {
  default = "YOUR_BILLING_ID_HERE"
}

variable "allowed_source_ip" {
  default = "YOUR_IP_HERE/32"
}

```




### 2. Initialize Terraform

Open your terminal in the directory containing `main.tf` and `variables.tf`, then run:

```bash
terraform init

```

*This downloads the necessary Google Cloud providers.*

### 3. Review the Plan

Before applying changes, verify exactly what Terraform will create:

```bash
terraform plan

```

**Check for:**

* Creation of the VPC and Firewall.
* The `g2-standard-4` instance with an NVIDIA L4 GPU.
* The automatic stop policy (11:00 PM EST).

### 4. Deploy the Lab

Execute the deployment:

```bash
terraform apply

```

*Type `yes` when prompted.*

---

## 🚀 Post-Deployment

### Startup Script Progress

The VM will start immediately, but the **Startup Script** (installing NVIDIA drivers, Ollama, and Garak) takes **10–15 minutes** to complete because it pulls several GBs of LLM models.

To watch the progress, SSH into your VM and run:

```bash
sudo journalctl -u google-startup-scripts.service -f

```

### Accessing the Lab

Once finished, you can access your Streamlit app at:
`http://[YOUR_VM_EXTERNAL_IP]:8501`

---

## 💰 Cost Management & Cleanup

* **Auto-Stop:** The instance is scheduled to stop at **11 PM EST** daily to save costs.
* **GPU Cost:** Remember that GPUs (NVIDIA L4) are billed while the VM is running.
* **Full Deletion:** To avoid all charges when finished with the lab:
```bash
terraform destroy

```



---
