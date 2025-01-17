# Key Management Architecture

## Overview

This document details the key management architecture of the YubiKey-Based Autonomous Sub-Key Network, focusing on the hierarchical structure, lifecycle management, and security procedures for all cryptographic keys in the system.

## Key Hierarchy

### 1. Master Key (Root of Trust)

#### Characteristics
- 4096-bit RSA key pair
- Stored exclusively in Master YubiKey
- Never exported or backed up
- Used only for signing sub-keys

#### Operations
- Sub-key signing
- Key revocation
- Certificate generation
- Trust chain establishment

### 2. Device Sub-Keys

#### Properties
- 2048-bit RSA or ECC keys
- Generated per device
- Hardware-bound to device YubiKey
- Regular rotation schedule

#### Usage
- Traffic encryption
- Authentication signatures
- Session key generation
- Secure communication

### 3. Router Sub-Keys

#### Configuration
- 2048-bit RSA or ECC keys
- Router-specific generation
- Hardware-bound to router YubiKey
- Automated rotation

#### Functions
- Traffic decryption
- Device authentication
- External tunnel establishment
- Network security

### 4. Session Keys

#### Specifications
- 256-bit AES keys
- Ephemeral generation
- Unique per session
- Time-limited validity

#### Application
- Data encryption
- Traffic protection
- Temporary secure channels
- Forward secrecy

## Key Lifecycle Management

### 1. Key Generation

#### Master Key
```bash
# Master key generation (performed once)
gpg --card-edit
admin
generate
```

#### Sub-Keys
```bash
# Device/Router sub-key generation
gpg --edit-key [MASTER_KEY_ID]
addkey
```

### 2. Key Distribution

#### Process Flow
1. Sub-key generation on server
2. Secure transfer to YubiKey
3. Verification of installation
4. Activation in system

#### Security Measures
- Encrypted channels
- Hardware verification
- Integrity checks
- Audit logging

### 3. Key Rotation

#### Schedule
- Master Key: No rotation (hardware-bound)
- Device Sub-Keys: 6-month rotation
- Router Sub-Keys: 3-month rotation
- Session Keys: Per-session generation

#### Procedures
1. New key generation
2. Old key preservation
3. System update
4. Old key revocation

### 4. Key Revocation

#### Triggers
- Security breach
- Device compromise
- Regular rotation
- System updates

#### Process
1. Revocation certificate generation
2. Key deactivation
3. System notification
4. New key deployment

## Security Controls

### 1. Access Control

#### Physical Security
- YubiKey physical protection
- Server security
- Hardware isolation
- Access logging

#### Logical Security
- Authentication requirements
- Authorization levels
- Operation logging
- Audit trails

### 2. Monitoring

#### System Checks
- Key usage monitoring
- Operation logging
- Anomaly detection
- Performance tracking

#### Alerts
- Unauthorized access attempts
- Key operation failures
- System anomalies
- Critical events

### 3. Backup and Recovery

#### Backup Procedures
- Sub-key backup policies
- Recovery procedures
- Emergency protocols
- System restoration

#### Recovery Process
1. Incident assessment
2. Backup verification
3. System restoration
4. Key redeployment

## Implementation Guidelines

### 1. YubiKey Configuration

#### Initial Setup
```bash
# YubiKey initialization
gpg --card-edit
admin
passwd
```

#### Key Import
```bash
# Sub-key import to YubiKey
gpg --edit-key [KEY_ID]
keytocard
```

### 2. Server Configuration

#### GPG Agent Setup
```bash
# gpg-agent configuration
echo "enable-ssh-support" >> ~/.gnupg/gpg-agent.conf
echo "default-cache-ttl 600" >> ~/.gnupg/gpg-agent.conf
```

#### Monitoring Setup
```bash
# Log configuration
echo "log-file ~/.gnupg/gpg.log" >> ~/.gnupg/gpg.conf
echo "debug-level basic" >> ~/.gnupg/gpg.conf
```

## Best Practices

### 1. Key Generation

- Use strong random number generation
- Verify key integrity
- Document all procedures
- Maintain secure environment

### 2. Key Storage

- Use hardware security only
- Implement access controls
- Regular security audits
- Maintain key inventory

### 3. Key Usage

- Limit key operations
- Monitor key usage
- Regular key verification
- Usage logging

### 4. Emergency Procedures

- Document recovery steps
- Regular testing
- Team training
- Incident response 