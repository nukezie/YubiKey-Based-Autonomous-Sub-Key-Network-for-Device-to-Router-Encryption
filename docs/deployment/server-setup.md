# Server Setup Guide

## Overview

This document provides detailed instructions for setting up and configuring the server infrastructure for the YubiKey-Based Autonomous Sub-Key Network.

## Server Requirements

### 1. Hardware Requirements

#### Minimum Specifications
- CPU: 8 cores, 3.0GHz+
- RAM: 32GB
- Storage: 500GB SSD
- Network: 10Gbps NIC

#### Recommended Specifications
- CPU: 16 cores, 3.5GHz+
- RAM: 64GB
- Storage: 1TB NVMe SSD
- Network: Dual 10Gbps NICs

### 2. Software Requirements

#### Operating System
- Ubuntu Server 22.04 LTS or later
- Security-hardened configuration
- Regular security updates
- Minimal installation

#### Required Packages
```bash
# System packages
apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    nginx \
    postgresql \
    redis-server \
    supervisor \
    ufw \
    fail2ban

# Python packages
pip3 install -r requirements.txt
```

## Initial Setup

### 1. System Configuration

#### Security Hardening
```bash
# Update system
apt-get update && apt-get upgrade -y

# Configure firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow https
ufw enable

# Configure fail2ban
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
systemctl enable fail2ban
systemctl start fail2ban
```

#### Network Configuration
```bash
# Configure network interfaces
cat > /etc/netplan/50-cloud-init.yaml << EOF
network:
    version: 2
    ethernets:
        ens160:
            dhcp4: no
            addresses: [192.168.1.100/24]
            gateway4: 192.168.1.1
            nameservers:
                addresses: [8.8.8.8, 8.8.4.4]
EOF

# Apply network configuration
netplan apply
```

### 2. Database Setup

#### PostgreSQL Configuration
```bash
# Create database
sudo -u postgres psql << EOF
CREATE DATABASE yubikey_network;
CREATE USER yubikey_admin WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE yubikey_network TO yubikey_admin;
EOF

# Configure PostgreSQL
cat > /etc/postgresql/14/main/postgresql.conf << EOF
listen_addresses = 'localhost'
max_connections = 1000
shared_buffers = 8GB
work_mem = 32MB
maintenance_work_mem = 256MB
effective_cache_size = 24GB
EOF
```

#### Redis Configuration
```bash
# Configure Redis
cat > /etc/redis/redis.conf << EOF
bind 127.0.0.1
port 6379
maxmemory 8gb
maxmemory-policy allkeys-lru
EOF

# Start Redis
systemctl enable redis-server
systemctl start redis-server
```

## Application Deployment

### 1. Application Setup

#### Directory Structure
```bash
# Create application directories
mkdir -p /opt/yubikey-network/{app,config,logs,data}
chown -R yubikey:yubikey /opt/yubikey-network

# Create log directories
mkdir -p /var/log/yubikey-network
chown -R yubikey:yubikey /var/log/yubikey-network
```

#### Configuration Files
```bash
# Application configuration
cat > /opt/yubikey-network/config/app.yaml << EOF
server:
  host: 0.0.0.0
  port: 8000
  workers: 4

database:
  host: localhost
  port: 5432
  name: yubikey_network
  user: yubikey_admin

redis:
  host: localhost
  port: 6379
  db: 0

security:
  key_rotation_days: 180
  session_timeout: 3600
  max_failed_attempts: 3
EOF
```

### 2. Service Configuration

#### Supervisor Setup
```bash
# Configure supervisor
cat > /etc/supervisor/conf.d/yubikey-network.conf << EOF
[program:yubikey-network]
command=/opt/yubikey-network/venv/bin/python app.py
directory=/opt/yubikey-network/app
user=yubikey
autostart=true
autorestart=true
stderr_logfile=/var/log/yubikey-network/error.log
stdout_logfile=/var/log/yubikey-network/access.log
EOF

# Start supervisor
supervisorctl reread
supervisorctl update
```

#### Nginx Configuration
```bash
# Configure Nginx
cat > /etc/nginx/sites-available/yubikey-network << EOF
server {
    listen 443 ssl http2;
    server_name yubikey-network.local;

    ssl_certificate /etc/ssl/certs/yubikey-network.crt;
    ssl_certificate_key /etc/ssl/private/yubikey-network.key;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/yubikey-network /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx
```

## Security Configuration

### 1. SSL/TLS Setup

#### Certificate Generation
```bash
# Generate SSL certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/yubikey-network.key \
    -out /etc/ssl/certs/yubikey-network.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=yubikey-network.local"

# Set permissions
chmod 600 /etc/ssl/private/yubikey-network.key
chmod 644 /etc/ssl/certs/yubikey-network.crt
```

#### TLS Configuration
```bash
# Configure SSL parameters
cat > /etc/nginx/conf.d/ssl.conf << EOF
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
EOF
```

### 2. Firewall Configuration

#### UFW Rules
```bash
# Configure firewall rules
ufw allow from 192.168.1.0/24 to any port 5432 # PostgreSQL
ufw allow from 192.168.1.0/24 to any port 6379 # Redis
ufw allow 443/tcp # HTTPS
ufw enable
```

#### Fail2ban Configuration
```bash
# Configure fail2ban
cat > /etc/fail2ban/jail.local << EOF
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600

[yubikey-network]
enabled = true
port = https
filter = yubikey-network
logpath = /var/log/yubikey-network/access.log
maxretry = 5
bantime = 3600
EOF
```

## Monitoring Setup

### 1. System Monitoring

#### Prometheus Configuration
```bash
# Configure Prometheus
cat > /etc/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'yubikey-network'
    static_configs:
      - targets: ['localhost:8000']
EOF
```

#### Grafana Setup
```bash
# Configure Grafana
cat > /etc/grafana/provisioning/dashboards/yubikey-network.yaml << EOF
apiVersion: 1
providers:
  - name: 'YubiKey Network'
    folder: ''
    type: file
    options:
      path: /var/lib/grafana/dashboards
EOF
```

### 2. Log Management

#### Logrotate Configuration
```bash
# Configure log rotation
cat > /etc/logrotate.d/yubikey-network << EOF
/var/log/yubikey-network/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 yubikey yubikey
    sharedscripts
    postrotate
        supervisorctl restart yubikey-network
    endscript
}
EOF
```

#### Audit Logging
```bash
# Configure audit logging
cat > /etc/audit/rules.d/yubikey-network.rules << EOF
-w /opt/yubikey-network/config -p wa -k yubikey_config
-w /opt/yubikey-network/data -p wa -k yubikey_data
EOF

# Reload audit rules
auditctl -R /etc/audit/rules.d/yubikey-network.rules
```

## Maintenance Procedures

### 1. Backup Configuration

#### Database Backup
```bash
# Configure automated backups
cat > /etc/cron.daily/yubikey-backup << EOF
#!/bin/bash
BACKUP_DIR="/var/backups/yubikey-network"
DATE=\$(date +%Y%m%d)

# Backup database
pg_dump yubikey_network | gzip > \$BACKUP_DIR/db_\$DATE.gz

# Backup configuration
tar czf \$BACKUP_DIR/config_\$DATE.tar.gz /opt/yubikey-network/config

# Rotate old backups
find \$BACKUP_DIR -type f -mtime +30 -delete
EOF

chmod +x /etc/cron.daily/yubikey-backup
```

#### System State Backup
```bash
# Configure system state backup
cat > /etc/cron.weekly/system-backup << EOF
#!/bin/bash
BACKUP_DIR="/var/backups/system"
DATE=\$(date +%Y%m%d)

# Backup system configuration
tar czf \$BACKUP_DIR/system_\$DATE.tar.gz \
    /etc/nginx \
    /etc/supervisor \
    /etc/prometheus \
    /etc/grafana

# Rotate old backups
find \$BACKUP_DIR -type f -mtime +90 -delete
EOF

chmod +x /etc/cron.weekly/system-backup
``` 