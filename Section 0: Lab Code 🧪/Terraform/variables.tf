variable "project_id" {
  description = "The GCP Project ID"
  type        = string
  default     = "coral-mission-481512-i4"
}

variable "region" {
  type    = string
  default = "us-west1"
}

variable "zone" {
  type    = string
  default = "us-west1-a"
}

variable "billing_account_id" {
  description = "Billing Account ID"
  type        = string
  default     = "01C828-DE9175-48B6B1"
}

variable "allowed_source_ip" {
  description = "Your Public IP (e.g. 1.2.3.4/32)"
  type        = string
  default     = "x.x.x.x/32"
}
