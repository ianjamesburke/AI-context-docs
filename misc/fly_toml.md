# Fly.io Configuration Cheat Sheet

```toml
# Basic Config
app = "my-app-name"
primary_region = "ord"

# Runtime Options
kill_signal = "SIGTERM"
kill_timeout = 120  # in seconds

# Console Command
console_command = "/app/manage.py shell"

# Swap Size
swap_size_mb = 512

# Build Section
[build]
builder = "paketobuildpacks/builder:base"
buildpacks = ["gcr.io/paketo-buildpacks/nodejs"]

# Using Docker Image
[build]
image = "flyio/hellofly:latest"

# Using Dockerfile
[build]
dockerfile = "Dockerfile.test"

# Deployment Options
[deploy]
release_command = "bin/rails db:migrate"
strategy = "bluegreen"
wait_timeout = "10m"

# Environment Variables
[env]
LOG_LEVEL = "debug"
RAILS_ENV = "production"

# HTTP Service
[http_service]
internal_port = 8080
force_https = true
min_machines_running = 1

[http_service.concurrency]
type = "requests"
soft_limit = 200
hard_limit = 250

# HTTP Options
[http_service.http_options]
idle_timeout = 600
h2_backend = true

[http_service.http_options.response]
pristine = true

# Services Configuration
[[services]]
internal_port = 8080
protocol = "tcp"
auto_stop_machines = "stop"
auto_start_machines = true

[[services.ports]]
handlers = ["http"]
port = 80
force_https = true

# TLS Options
[[services.ports]]
handlers = ["tls", "http"]
port = 443
tls_options = { "alpn" = ["h2", "http/1.1"], "versions" = ["TLSv1.2", "TLSv1.3"] }

# Concurrency Limits
[services.concurrency]
type = "connections"
hard_limit = 25
soft_limit = 20

# Health Checks
[[services.http_checks]]
interval = "10s"
timeout = "2s"
method = "GET"
path = "/health"

[[services.tcp_checks]]
interval = "15s"
timeout = "2s"

# Volume Mounts
[mounts]
source = "myapp_data"
destination = "/data"
snapshot_retention = 14

# Auto Extend Volume Size
[[mounts]]
auto_extend_size_threshold = 80
auto_extend_size_increment = "1GB"
auto_extend_size_limit = "5GB"

# VM Configuration
[vm]
cpu_count = 2
memory_size_mb = 2048
```
```
