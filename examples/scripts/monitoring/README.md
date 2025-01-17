# YubiKey Network Monitoring Tool

This tool implements monitoring, metrics collection, and alerting for the YubiKey-Based Autonomous Sub-Key Network.

## Features

- Real-time YubiKey health monitoring
- Authentication and session metrics
- Performance metrics collection
- Configurable alerting system
- Integration with Prometheus
- Email and Slack notifications

## Prerequisites

- Python 3.8 or higher
- Prometheus server (for metrics storage)
- SMTP server (for email alerts)
- Slack webhook (for Slack alerts)
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

The main configuration file (`config.yml`) contains settings for:
- Metrics collection
- YubiKey devices to monitor
- Alert channels
- Email and Slack settings
- Logging configuration
- Performance thresholds
- Security settings

Example:
```yaml
metrics_port: 9090
collection_interval: 30
yubikeys:
  - device-yubikey-1
  - router-yubikey-1
```

### Alert Rules (alert_rules.yml)

Alert rules are defined in `alert_rules.yml` and include:
- Health alerts
- Authentication alerts
- Performance alerts
- Security alerts

Example rule:
```yaml
- name: YubiKeyUnhealthy
  type: threshold
  metric: yubikey_health
  comparison: below
  threshold: 1
  severity: critical
```

## Usage

Start the monitoring service:
```bash
python monitor_yubikey_network.py --config config.yml
```

Enable debug logging:
```bash
python monitor_yubikey_network.py --config config.yml --debug
```

## Metrics

### YubiKey Operations
- Total operations count
- Operation success/failure rates
- Operation latency

### Health Metrics
- YubiKey device health status
- Connection status
- Error rates

### Authentication Metrics
- Authentication success/failure rates
- Session counts
- Key usage statistics

## Alerting

### Channels
- Email notifications
- Slack messages

### Alert Types
1. **Critical Alerts**
   - YubiKey health issues
   - Authentication security violations
   - Unauthorized access attempts

2. **Warning Alerts**
   - High latency
   - Excessive sessions
   - Key rotation reminders

## Monitoring Dashboard

The tool exposes metrics in Prometheus format at:
```
http://localhost:9090/metrics
```

Recommended Grafana dashboards are available for:
- System Overview
- Security Metrics
- Performance Monitoring

## Security Considerations

1. **Access Control**
   - Restrict access to monitoring endpoints
   - Secure alert channels
   - Protect configuration files

2. **Data Protection**
   - Encrypt sensitive metrics
   - Secure alert delivery
   - Safe logging practices

3. **Integration Security**
   - Use secure SMTP
   - Validate Slack webhooks
   - Protect Prometheus endpoints

## Troubleshooting

Common issues and solutions:

1. **Metric Collection Failures**
   - Check YubiKey connectivity
   - Verify permissions
   - Review log files

2. **Alert Delivery Issues**
   - Verify SMTP settings
   - Check Slack webhook validity
   - Confirm network connectivity

3. **Performance Issues**
   - Adjust collection intervals
   - Optimize metric storage
   - Review resource usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.