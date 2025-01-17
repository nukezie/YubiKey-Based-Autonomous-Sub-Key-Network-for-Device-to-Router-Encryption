# YubiKey Network Backup Tool

This tool implements automated backup and recovery procedures for the YubiKey-Based Autonomous Sub-Key Network.

## Features

- Complete system backup and restore
- Encrypted backups using Fernet
- Key and certificate backup
- Configuration backup
- Database backup (PostgreSQL)
- State backup (Redis)
- Email and Slack notifications
- Automated retention management

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Redis server
- GPG installed and configured
- Required Python packages (see requirements.txt)

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

The configuration file contains settings for:
- Backup paths and retention
- Database connection
- Redis connection
- SSL certificates
- Encryption settings
- Notification channels

Example:
```yaml
backup:
  path: /var/backups/yubikey-network
  encrypt_backups: true
  key_file: /etc/yubikey-network/backup.key
  retention_days: 30
```

## Usage

### Create Backup
```bash
python backup_yubikey_network.py --config config.yml --action backup
```

### Restore from Backup
```bash
python backup_yubikey_network.py --config config.yml --action restore --backup-path /path/to/backup.tar.gz
```

### Enable Debug Logging
```bash
python backup_yubikey_network.py --config config.yml --action backup --debug
```

## Backup Components

### 1. Keys and Certificates
- GPG keys (public and private)
- SSL certificates
- YubiKey-related keys

### 2. Configuration Files
- Server configuration
- YubiKey configuration
- Network settings
- Security policies

### 3. Database
- PostgreSQL database dump
- Table structures
- Data records
- Indexes and constraints

### 4. System State
- Redis data
- Session information
- Cache data
- Runtime configurations

## Security Considerations

1. **Encryption**
   - All backups are encrypted by default
   - Secure key storage
   - Strong encryption algorithms

2. **Access Control**
   - Restricted backup locations
   - Secure key file permissions
   - Limited database access

3. **Data Protection**
   - Encrypted transport
   - Secure storage
   - Proper key management

## Backup Retention

The tool manages backup retention automatically:
- Keeps backups for configured number of days
- Removes old backups
- Maintains backup history

## Notifications

### Email Notifications
- Backup completion status
- Restore operation results
- Error notifications

### Slack Notifications
- Real-time backup status
- Operation completion
- Error alerts

## Troubleshooting

Common issues and solutions:

1. **Backup Failures**
   - Check disk space
   - Verify database connection
   - Check permissions
   - Review error logs

2. **Restore Failures**
   - Verify backup file integrity
   - Check encryption keys
   - Confirm system compatibility
   - Review restore logs

3. **Permission Issues**
   - Check file permissions
   - Verify user access
   - Review directory ownership

## Best Practices

1. **Regular Testing**
   - Test backup process regularly
   - Verify restore functionality
   - Validate backup integrity

2. **Monitoring**
   - Monitor backup success/failure
   - Track backup sizes
   - Monitor retention cleanup

3. **Documentation**
   - Document backup configurations
   - Maintain restore procedures
   - Keep encryption keys secure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 