output "project_id" {
  value = var.project_id
}

output "region" {
  value = var.region
}

output "backend_url" {
  value = "https://api.${var.environment}.edugenie.io"
}

output "frontend_url" {
  value = "https://${var.environment}.edugenie.io"
}
