# YubiKey Network Deployment Tools

This directory contains deployment tools and configuration files for setting up the YubiKey-Based Autonomous Sub-Key Network.

## Features

- Automated system deployment
- Service configuration
- Database setup
- Redis setup
- SSL/TLS configuration
- YubiKey initialization
- Monitoring setup
- Security hardening

## Prerequisites

- Ubuntu Server 22.04 LTS or later
- Python 3.8 or higher
- Root or sudo access
- Required system packages:
  - postgresql
  - redis-server
  - nginx
  - supervisor
  - gpg

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Main Configuration (config.yml)

The deployment configuration file contains settings for:
- System paths
- Database settings
- Redis configuration
- SSL certificates
- YubiKey settings
- Service parameters
- Security policies

Example:
```yaml
paths:
  config_dir: /etc/yubikey-network
  data_dir: /var/lib/yubikey-network
  log_dir: /var/log/yubikey-network
```

## Usage

### Deploy System
```bash
python deploy_yubikey_network.py --config config.yml
```

### Enable Debug Logging
```bash
python deploy_yubikey_network.py --config config.yml --debug
```

## Components

### 1. System Services
- `yubikey-network.service`: Main application service
- `yubikey-monitor.service`: Monitoring service

### 2. Web Server
- Nginx configuration with SSL/TLS
- Reverse proxy settings
- Security headers
- Rate limiting

### 3. Database
- PostgreSQL setup
- User creation
- Schema initialization
- Connection pooling

### 4. Cache
- Redis configuration
- Memory management
- Persistence settings

### 5. Monitoring
- Prometheus metrics
- Grafana dashboards
- Health checks
- Performance monitoring

## Security

### 1. System Hardening
- Minimal permissions
- Service isolation
- Secure defaults
- Regular updates

### 2. SSL/TLS
- Strong cipher suites
- Modern protocols
- Perfect forward secrecy
- HSTS enabled

### 3. Access Control
- Authentication required
- Rate limiting
- IP restrictions
- Secure headers

## Service Management

### Start Services
```bash
systemctl start yubikey-network
systemctl start yubikey-monitor
```

### Check Status
```bash
systemctl status yubikey-network
systemctl status yubikey-monitor
```

### View Logs
```bash
journalctl -u yubikey-network
journalctl -u yubikey-monitor
```

## Troubleshooting

Common issues and solutions:

1. **Service Start Failures**
   - Check service logs
   - Verify permissions
   - Validate configuration
   - Check dependencies

2. **Database Issues**
   - Verify PostgreSQL running
   - Check credentials
   - Review connection settings
   - Validate schema

3. **YubiKey Problems**
   - Check USB connection
   - Verify permissions
   - Test with ykman
   - Review logs

## Best Practices

1. **Pre-deployment**
   - Review configuration
   - Backup existing data
   - Test in staging
   - Verify prerequisites

2. **Security**
   - Change default passwords
   - Update SSL certificates
   - Configure firewalls
   - Enable monitoring

3. **Maintenance**
   - Regular backups
   - Monitor logs
   - Update packages
   - Test recovery

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 