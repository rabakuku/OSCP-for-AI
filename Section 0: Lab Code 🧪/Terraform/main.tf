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

    wget "https://raw.githubusercontent.com/rabakuku/OSCP-for-AI/refs/heads/main/Section%200%3A%20Lab%20Code%20%F0%9F%A7%AA/Terraform/installation_script.sh"
    chmod +x installation_script.sh
    ./installation_script.sh



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
