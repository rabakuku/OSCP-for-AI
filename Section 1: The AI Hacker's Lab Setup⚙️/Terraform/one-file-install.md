
---

# 🚀 Course Lab Environment Setup (Automated)

This repository contains the **Terraform** configuration to automatically deploy your Google Cloud Lab environment for the course.

## What This Deploys

* **Virtual Machine:** `g2-standard-4` (NVIDIA L4 GPU) with Deep Learning Image.
* **Networking:** Custom VPC with Firewall rules restricting access to *your* IP only.
* **Cost Controls:** * **Auto-Shutdown Schedule:** Stops the VM automatically at 11:00 PM EST every night.
* **Budget Alert:** Notifies you if monthly costs exceed specific thresholds ($78, $156, $260).
* **No Snapshots:** Snapshots are disabled to prevent hidden storage costs.


* **Automation:** Automatically installs necessary course files and requirements on first boot.

---

## ⚠️ Prerequisites (Read Before Starting)

1. **Google Cloud Account:** You must have an active GCP account with billing enabled.
2. **GPU Quota:** New accounts often have a quota of **0 GPUs**.
* **Check:** Go to **IAM & Admin > Quotas & System Limits**.
* **Search:** "NVIDIA L4 GPUs".
* **Action:** If the limit is 0, request an increase to **1** in the `us-central1` region. (Approvals take 24-48 hours).


3. **Cost Warning:** This VM costs approximately **$1.50 - $2.00 per hour**. While the auto-shutdown helps, **always manually stop your instance** when you are done studying to save money.

---

## 🛠️ Installation Guide

We will use **Google Cloud Shell** because Terraform is pre-installed. You do not need to install anything on your computer.

### Step 1: Open Cloud Shell

1. Log in to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the **Terminal Icon** `>_` in the top right corner of the navigation bar.

### Step 2: Create Files

Run the following commands in the terminal to create your directory and files:

```bash
mkdir oscp-lab
cd oscp-lab
touch main.tf variables.tf terraform.tfvars

```

### Step 3: Edit `main.tf`

Click the **"Open Editor"** button (pencil icon) in the terminal to open the code editor. Paste the following code into `main.tf`:

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# -------------------------------------------------------------------
# 1. NETWORK & FIREWALL
# -------------------------------------------------------------------
resource "google_compute_network" "vpc_network" {
  name                    = "udemy-course-vpc"
  auto_create_subnetworks = true
}

resource "google_compute_firewall" "allow_oscp_for_ai" {
  name    = "allow-oscp-for-ai-server"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22", "8501"] # SSH + Streamlit/App port
  }

  # Allows Google IAP + The Student's IP Address (from terraform.tfvars)
  source_ranges = [
    "35.235.240.0/20",     # Google IAP (Identity-Aware Proxy)
    var.allowed_source_ip  # The Student's Personal IP
  ]

  target_tags = ["oscp-for-ai-server"]
}

# -------------------------------------------------------------------
# 2. INSTANCE SCHEDULE (AUTO STOP)
# -------------------------------------------------------------------
resource "google_compute_resource_policy" "oscp_stop_policy" {
  name        = "oscp-for-ai-stop-at-11"
  region      = var.region
  description = "Stopping my Instance call OSCP-For-AI at 11 p.m. EST time."

  instance_schedule_policy {
    # 23:00 = 11 PM
    vm_stop_schedule {
      schedule = "0 23 * * *"
    }
    time_zone = "America/New_York"
  }
}

# -------------------------------------------------------------------
# 3. VIRTUAL MACHINE (oscp-for-ai)
# -------------------------------------------------------------------
resource "google_compute_instance" "oscp_for_ai" {
  name         = "oscp-for-ai"
  machine_type = "g2-standard-4" # GPU Instance (NVIDIA L4)
  zone         = var.zone

  tags = ["oscp-for-ai-server"]

  boot_disk {
    initialize_params {
      # OPTION 2 (SAFE MODE): Using Standard Debian 11.
      # This image always exists. The startup script below will install the GPU drivers.
      image = "debian-cloud/debian-11"
      size  = 100
      type  = "pd-ssd"
    }
    auto_delete = true
  }

  # GPU Configuration
  guest_accelerator {
    type  = "nvidia-l4"
    count = 1
  }

  # GPU instances require this specific maintenance policy
  scheduling {
    on_host_maintenance = "TERMINATE"
    automatic_restart   = true
    provisioning_model  = "STANDARD"
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
      network_tier = "PREMIUM"
    }
  }

  metadata = {
    enable-osconfig = "TRUE"
  }

  # ---------------------------------------------------------
  # STARTUP SCRIPT (Runs automatically on first boot as root)
  # ---------------------------------------------------------
  metadata_startup_script = <<-EOT
    #! /bin/bash
    
    # 1. Install NVIDIA Drivers (REQUIRED for this Image)
    # -------------------------------------------------
    echo "Starting NVIDIA Driver Installation..."
    # Downloads Google's official script to install the correct driver for L4 GPUs
    curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py --output install_gpu_driver.py
    # Runs the installer
    python3 install_gpu_driver.py

    # 2. Prepare the Lab Environment
    # ------------------------------
    echo "Setting up Course Files..."
    mkdir -p oscp-for-ai
    cd oscp-for-ai

    # Download files (Quotes added to handle spaces and emojis in URL)
    wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section 0%3A Lab Code 🧪/setup.sh"
    wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section 0%3A Lab Code 🧪/requirements.txt"

    # Make executable and run
    chmod +x setup.sh
    ./setup.sh
  EOT

  service_account {
    scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring.write",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/trace.append"
    ]
  }

  shielded_instance_config {
    enable_secure_boot          = false
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }

  # Attach the schedule policy here
  resource_policies = [google_compute_resource_policy.oscp_stop_policy.id]
}

# -------------------------------------------------------------------
# 4. BUDGET ALERT
# -------------------------------------------------------------------
resource "google_billing_budget" "budget_alert" {
  billing_account = var.billing_account_id
  display_name    = "Course-VM-Budget"

  budget_filter {
    projects               = ["projects/${var.project_id}"]
    credit_types_treatment = "EXCLUDE_ALL_CREDITS"
    calendar_period        = "MONTH"
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = "260"
    }
  }

  threshold_rules {
    threshold_percent = 0.3
  }
  threshold_rules {
    threshold_percent = 0.6
  }
  threshold_rules {
    threshold_percent = 0.9
  }
  threshold_rules {
    threshold_percent = 1.0
  }
}
```

### Step 4: Edit `variables.tf`

Paste the following into `variables.tf`:

```hcl
variable "project_id" { description = "The GCP Project ID" }
variable "region" { default = "us-central1" }
variable "zone" { default = "us-central1-c" }
variable "billing_account_id" { description = "Billing Account ID" }
variable "allowed_source_ip" { description = "Your Public IP (e.g. 1.2.3.4/32)" }

```

### Step 5: Configure YOUR Settings (`terraform.tfvars`)

Paste the following into `terraform.tfvars` and **change the values** to match your info:

```hcl
# 1. Your Project ID (NOT the name)
project_id = "my-project-id-12345"

# 2. Your Billing Account ID (Find this in the Billing Console)
# get account id via shell with command gcloud billing accounts list
billing_account_id = "000000-000000-000000"

# 3. Your Public IP Address (Google "What is my IP")
# IMPORTANT: You MUST add /32 at the end
allowed_source_ip = "12.34.56.78/32"

# 4. Deployment Zone
zone = "us-central1-c"

```

### Step 6: Deploy!

Run these commands in your terminal:

```bash
# Initialize Terraform
terraform init

# Apply the configuration (Type 'yes' when asked)
terraform apply

```

---

## ❓ Troubleshooting

### Error: `ZONE_RESOURCE_POOL_EXHAUSTED`

This means `us-central1-c` is out of GPUs right now.

1. Open `terraform.tfvars`.
2. Change `zone = "us-central1-c"` to `"us-central1-a"` or `"us-central1-b"`.
3. Run `terraform apply` again.

### Error: `QUOTA_EXCEEDED`

This means your account is not allowed to use GPUs yet. See the **Prerequisites** section above to request a quota increase.

### How to Delete Everything

To stop costs completely when you finish the course, run:

```bash
terraform destroy

```
