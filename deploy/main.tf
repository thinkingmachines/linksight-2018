variable "instance_name" {}

variable "machine_type" {
  default = "n1-standard-2"
}

provider "google-beta" {
  project = "linksight-208514"
  region  = "us-east1"
}

resource "google_compute_address" "static" {
  provider = "google-beta"
  name     = "${var.instance_name}"
}

resource "google_compute_instance" "instance" {
  provider                  = "google-beta"
  name                      = "${var.instance_name}"
  machine_type              = "n1-standard-1"
  zone                      = "us-east1-b"
  tags                      = ["http-server", "https-server", "docker"]
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = "${google_compute_address.static.address}"
    }
  }

  service_account {
    scopes = ["cloud-platform", "https://www.googleapis.com/auth/drive.readonly"]
  }
}

output "ip" {
  value = "${google_compute_address.static.address}"
}
