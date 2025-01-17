# System Monitoring Guide

## Overview

This document details the monitoring and alerting system for the YubiKey-Based Autonomous Sub-Key Network, covering metrics collection, alerting, and incident response procedures.

## Monitoring Architecture

### 1. Core Components

#### Monitoring Stack
- Prometheus: Metrics collection and storage
- Grafana: Visualization and dashboards
- AlertManager: Alert routing and notification
- Node Exporter: System metrics collection
- Custom Exporters: YubiKey-specific metrics

#### Directory Structure
```bash
/opt/yubikey-network/
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── alerts.yml
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── datasources/
│   └── alertmanager/
│       └── alertmanager.yml
```

## Metrics Collection

### 1. System Metrics

#### Node Exporter Configuration
```yaml
# /etc/prometheus/node_exporter.yml
---
collectors:
  enabled:
    - cpu
    - diskstats
    - filesystem
    - loadavg
    - meminfo
    - netdev
    - systemd
    - uname
```

#### Custom YubiKey Metrics
```python
from prometheus_client import Counter, Gauge, Histogram

# YubiKey Operations
yubikey_operations = Counter(
    'yubikey_operations_total',
    'Total number of YubiKey operations',
    ['operation_type', 'status']
)

# YubiKey Health
yubikey_health = Gauge(
    'yubikey_health_status',
    'YubiKey health status (1 = healthy, 0 = unhealthy)',
    ['yubikey_id']
)

# Operation Latency
operation_latency = Histogram(
    'yubikey_operation_duration_seconds',
    'Time spent processing YubiKey operations',
    ['operation_type']
)
```

### 2. Application Metrics

#### Performance Metrics
```python
class MetricsCollector:
    def __init__(self):
        self.auth_latency = Histogram(
            'auth_latency_seconds',
            'Authentication request latency'
        )
        self.key_ops = Counter(
            'key_operations_total',
            'Total number of key operations',
            ['operation_type']
        )
        self.active_sessions = Gauge(
            'active_sessions',
            'Number of active sessions'
        )
```

#### Security Metrics
```python
class SecurityMetrics:
    def __init__(self):
        self.auth_failures = Counter(
            'auth_failures_total',
            'Authentication failures',
            ['reason']
        )
        self.key_rotations = Counter(
            'key_rotations_total',
            'Key rotation events',
            ['key_type']
        )
        self.security_events = Counter(
            'security_events_total',
            'Security-related events',
            ['severity', 'type']
        )
```

## Alerting Configuration

### 1. Alert Rules

#### Prometheus Alert Rules
```yaml
# /etc/prometheus/alerts.yml
groups:
  - name: yubikey_alerts
    rules:
      - alert: YubiKeyUnhealthy
        expr: yubikey_health_status == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "YubiKey {{ $labels.yubikey_id }} is unhealthy"
          
      - alert: HighAuthFailureRate
        expr: rate(auth_failures_total[5m]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High authentication failure rate detected"
          
      - alert: KeyRotationOverdue
        expr: time() - last_key_rotation > 86400 * 180
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Key rotation is overdue"
```

#### AlertManager Configuration
```yaml
# /etc/alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'security-team'

receivers:
  - name: 'security-team'
    email_configs:
      - to: 'security@yubikey-network.local'
    slack_configs:
      - channel: '#security-alerts'
```

## Dashboard Configuration

### 1. Grafana Dashboards

#### System Overview
```json
{
  "dashboard": {
    "title": "YubiKey Network Overview",
    "panels": [
      {
        "title": "Active Sessions",
        "type": "graph",
        "targets": [
          {
            "expr": "active_sessions"
          }
        ]
      },
      {
        "title": "Authentication Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(auth_operations_total[5m])"
          }
        ]
      },
      {
        "title": "YubiKey Health Status",
        "type": "status-map",
        "targets": [
          {
            "expr": "yubikey_health_status"
          }
        ]
      }
    ]
  }
}
```

#### Security Dashboard
```json
{
  "dashboard": {
    "title": "Security Metrics",
    "panels": [
      {
        "title": "Authentication Failures",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(auth_failures_total[5m])"
          }
        ]
      },
      {
        "title": "Security Events",
        "type": "table",
        "targets": [
          {
            "expr": "security_events_total"
          }
        ]
      }
    ]
  }
}
```

## Log Management

### 1. Log Collection

#### Filebeat Configuration
```yaml
# /etc/filebeat/filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/yubikey-network/*.log
  fields:
    type: yubikey-network
  
output.elasticsearch:
  hosts: ["localhost:9200"]
  index: "yubikey-network-%{+yyyy.MM.dd}"
```

#### Log Formats
```python
def format_log_entry(event):
    return {
        'timestamp': time.time(),
        'level': event.level,
        'component': event.component,
        'message': event.message,
        'metadata': {
            'yubikey_id': event.yubikey_id,
            'operation': event.operation,
            'status': event.status
        }
    }
```

### 2. Log Analysis

#### Elasticsearch Templates
```json
{
  "index_patterns": ["yubikey-network-*"],
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "level": { "type": "keyword" },
      "component": { "type": "keyword" },
      "message": { "type": "text" },
      "metadata": {
        "properties": {
          "yubikey_id": { "type": "keyword" },
          "operation": { "type": "keyword" },
          "status": { "type": "keyword" }
        }
      }
    }
  }
}
```

## Incident Response

### 1. Alert Handling

#### Response Procedures
```python
class AlertHandler:
    def handle_alert(self, alert):
        if alert.severity == 'critical':
            self.notify_security_team(alert)
            self.initiate_incident_response(alert)
        elif alert.severity == 'warning':
            self.notify_operations_team(alert)
            self.create_incident_ticket(alert)
```

#### Escalation Matrix
```yaml
# /etc/yubikey-network/escalation.yml
escalation_levels:
  - level: 1
    team: operations
    response_time: 30m
    contacts:
      - ops@yubikey-network.local
      - "#ops-alerts"
      
  - level: 2
    team: security
    response_time: 15m
    contacts:
      - security@yubikey-network.local
      - "#security-alerts"
      
  - level: 3
    team: incident-response
    response_time: 5m
    contacts:
      - ir@yubikey-network.local
      - emergency-contacts
```

### 2. Automated Response

#### Response Actions
```python
class AutomatedResponse:
    def execute_response(self, alert):
        if alert.type == 'YubiKeyUnhealthy':
            self.attempt_yubikey_recovery(alert.yubikey_id)
        elif alert.type == 'HighAuthFailureRate':
            self.enable_enhanced_monitoring()
            self.adjust_rate_limits()
```

#### Recovery Procedures
```python
class RecoveryProcedures:
    async def recover_yubikey(self, yubikey_id):
        try:
            # Attempt recovery
            await self.reset_yubikey(yubikey_id)
            await self.reinitialize_yubikey(yubikey_id)
            await self.verify_yubikey_health(yubikey_id)
        except Exception as e:
            self.escalate_incident(yubikey_id, e)
``` 