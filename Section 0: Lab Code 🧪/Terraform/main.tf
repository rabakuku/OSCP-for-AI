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

  source_ranges = [
    "35.235.240.0/20",     # Google IAP
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
  tags         = ["oscp-for-ai-server"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 100
      type  = "pd-ssd"
    }
    auto_delete = true
  }

  guest_accelerator {
    type  = "nvidia-l4"
    count = 1
  }

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
    enable-osconfig       = "TRUE"
    install-nvidia-driver = "True"
  }

  # ---------------------------------------------------------
  # STARTUP SCRIPT (Runs automatically on first boot as root)
  # ---------------------------------------------------------
  metadata_startup_script = <<-EOT
    #! /bin/bash

    #if file is there, do not run starte up script again
    FLAG_FILE="/etc/startup_was_launched"

    if [[ -f "$FLAG_FILE" ]]; then
    echo "Startup script already ran once. Exiting."
    exit 0
    fi    

    # 2. Prepare the Lab Environment
    # ------------------------------
    echo "Setting up Course Files..."
    mkdir -p oscp-for-ai
    cd oscp-for-ai

    # Download files (Quotes added to handle spaces and emojis in URL)
    wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section 0%3A Lab Code 🧪/setup.sh"
    wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section 0%3A Lab Code 🧪/requirements.txt"
    sudo apt install git -y
    sudo apt-get install python3-venv -y
    sudo sed -i '/bullseye-backports/s/^/#/' /etc/apt/sources.list
    sudo apt update && sudo apt install -y python3-pip python3-venv git -y
    sudo curl -fsSL https://ollama.com/install.sh | sh
    sudo systemctl enable ollama.service
    sudo systemctl start ollama.service
    #Configure Ollama for Parallelism
    mkdir -p /etc/systemd/system/ollama.service.d
    echo "[Service]" > /etc/systemd/system/ollama.service.d/override.conf
    echo "Environment=\"OLLAMA_NUM_PARALLEL=16\"" >> /etc/systemd/system/ollama.service.d/override.conf
    echo "Environment=\"OLLAMA_MAX_LOADED_MODELS=1\"" >> /etc/systemd/system/ollama.service.d/override.conf
    echo "Environment=\"OLLAMA_KEEP_ALIVE=-1\"" >> /etc/systemd/system/ollama.service.d/override.conf

    echo "✅ Installation of Ollama is Complete!"

    sudo systemctl daemon-reload
    sudo systemctl restart ollama
    sudo ollama pull llama3
    sudo ollama pull llama-guard3
    sudo ollama pull llava
    sudo ollama pull dolphin-llama3
    sudo ollama pull mistral-nemo
    sudo ollama pull llama2-uncensored
    sudo ollama pull gemma:2b
    sudo ollama pull phi3:mini
    echo "✅ Downloaded all LLMS"


    # Make executable and run
    chmod +x setup.sh
    ./setup.sh
    echo "✅ Installation of Streamlit is Complete!"

    #install miniconda + garak
    wget https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%204%3A%20Automated%20Warfare/garak/setup_garak.sh
    chmod +x setup_garak.sh
    ./setup_garak.sh
echo "✅ Installation of garak is Complete!"

  #install and setup Giskard
cd /
mkdir giskard_lab
cd giskard_lab
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda create -n giskard_lab python=3.10 -y
conda activate giskard_lab
pip install "giskard[llm]" -y 
pip install langchain langchain-community pandas langchain-ollama -y 
echo "✅ Installation of Giskard is Complete!"


  #install and setup PyRIT
cd / 
mkdir PyRIT_lab
conda create -n PyRIT_lab python=3.11 -y
conda activate PyRIT_lab
cd PyRIT_lab
pip install pandas python-dotenv pyrit tabulate -y
wget https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%204%3A%20Automated%20Warfare/PyRIT/pyrit_master.py
echo "✅ Installation of PyRIT is Complete!"


  EOT

  service_account {
    scopes = ["cloud-platform"]
  }

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

  threshold_rules { threshold_percent = 0.3 }
  threshold_rules { threshold_percent = 0.6 }
  threshold_rules { threshold_percent = 0.9 }
  threshold_rules { threshold_percent = 1.0 }
}
