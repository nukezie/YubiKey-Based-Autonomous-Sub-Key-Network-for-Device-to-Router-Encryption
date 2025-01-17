# YubiKey Setup Guide

## Overview

This document provides detailed instructions for initializing and configuring YubiKeys for use in the YubiKey-Based Autonomous Sub-Key Network.

## Prerequisites

### 1. Required Software

#### System Packages
```bash
# Install required packages
apt-get update && apt-get install -y \
    yubikey-manager \
    yubico-piv-tool \
    opensc \
    pcsc-tools \
    scdaemon \
    gpg \
    gnupg2
```

#### Configuration Files
```bash
# Configure GPG for YubiKey
cat > ~/.gnupg/gpg-agent.conf << EOF
enable-ssh-support
default-cache-ttl 3600
max-cache-ttl 7200
EOF

# Configure scdaemon
cat > ~/.gnupg/scdaemon.conf << EOF
reader-port Yubico YubiKey
disable-ccid
EOF
```

## Master YubiKey Setup

### 1. Initial Configuration

#### Reset YubiKey
```bash
# Reset YubiKey to factory settings
ykman piv reset

# Reset OpenPGP application
gpg --card-edit
> admin
> factory-reset
```

#### Set PINs
```bash
# Set Management Key
ykman piv change-management-key \
    --generate \
    --protect

# Set PIN and PUK
ykman piv access change-pin
ykman piv access change-puk
```

### 2. Key Generation

#### Master Key Generation
```bash
# Generate master key
gpg --expert --full-generate-key
> (9) ECC and ECC
> (1) Curve 25519
> 0 (key does not expire)
> Real name: YubiKey Network Master
> Email: master@yubikey-network.local
> Comment: Master Key
```

#### Sub-Key Generation
```bash
# Generate sub-keys
gpg --expert --edit-key master@yubikey-network.local
> addkey
> (10) ECC (sign only)
> (1) Curve 25519
> 1y
> save

> addkey
> (12) ECC (encrypt only)
> (1) Curve 25519
> 1y
> save

> addkey
> (11) ECC (set your own capabilities)
> A (authentication only)
> (1) Curve 25519
> 1y
> save
```

## Device YubiKey Setup

### 1. Initial Setup

#### YubiKey Preparation
```bash
# Reset YubiKey
ykman piv reset

# Configure PIV
ykman piv access change-management-key \
    --protect \
    --generate

# Set device PIN
ykman piv access change-pin \
    --pin-policy always \
    --touch-policy always
```

#### Key Import
```bash
# Import device sub-key
gpg --edit-key device@yubikey-network.local
> keytocard
> save
```

### 2. Configuration

#### OpenPGP Configuration
```bash
# Configure OpenPGP application
gpg --card-edit
> admin
> name
> lang
> url
> login
> sex
> quit
```

#### Touch Policy
```bash
# Set touch policies
ykman openpgp set-touch sig fixed
ykman openpgp set-touch enc fixed
ykman openpgp set-touch aut fixed
```

## Router YubiKey Setup

### 1. Initial Configuration

#### Router Key Generation
```bash
# Generate router key
gpg --expert --full-generate-key
> (9) ECC and ECC
> (1) Curve 25519
> 1y
> Real name: YubiKey Network Router
> Email: router@yubikey-network.local
> Comment: Router Key
```

#### Key Import
```bash
# Import router key to YubiKey
gpg --edit-key router@yubikey-network.local
> keytocard
> save
```

### 2. Security Settings

#### Access Control
```bash
# Set access policies
ykman openpgp set-pin-retries 3 3 3
ykman openpgp set-touch sig fixed
ykman openpgp set-touch enc fixed
ykman openpgp set-touch aut fixed
```

#### Attestation
```bash
# Generate attestation certificate
ykman piv attest 9c > router-attestation.pem

# Verify attestation
ykman piv verify-attestation router-attestation.pem
```

## Key Management

### 1. Backup Procedures

#### Key Backup
```bash
# Export public keys
gpg --armor --export master@yubikey-network.local > master.pub
gpg --armor --export device@yubikey-network.local > device.pub
gpg --armor --export router@yubikey-network.local > router.pub

# Export private keys (secure storage required)
gpg --armor --export-secret-keys master@yubikey-network.local > master.key
gpg --armor --export-secret-subkeys device@yubikey-network.local > device.key
gpg --armor --export-secret-subkeys router@yubikey-network.local > router.key
```

#### Revocation Certificates
```bash
# Generate revocation certificates
gpg --gen-revoke master@yubikey-network.local > master-revoke.asc
gpg --gen-revoke device@yubikey-network.local > device-revoke.asc
gpg --gen-revoke router@yubikey-network.local > router-revoke.asc
```

### 2. Key Rotation

#### Rotation Schedule
```bash
# Create key rotation script
cat > rotate-keys.sh << EOF
#!/bin/bash

# Generate new sub-keys
gpg --edit-key master@yubikey-network.local
addkey
...

# Export new keys
gpg --armor --export master@yubikey-network.local > master-new.pub

# Update YubiKeys
ykman piv import-key ...
EOF

chmod +x rotate-keys.sh
```

#### Automation
```bash
# Add to crontab
echo "0 0 1 */6 * /path/to/rotate-keys.sh" >> /etc/crontab
```

## Verification Procedures

### 1. Key Verification

#### Signature Verification
```bash
# Test signature
echo "test" > test.txt
gpg --sign test.txt
gpg --verify test.txt.gpg

# Test encryption
gpg --encrypt --recipient device@yubikey-network.local test.txt
gpg --decrypt test.txt.gpg
```

#### Certificate Verification
```bash
# Verify certificates
ykman piv verify 9c device-cert.pem
ykman piv verify 9c router-cert.pem
```

### 2. Health Checks

#### YubiKey Status
```bash
# Check YubiKey status
ykman info
ykman openpgp info
ykman piv info

# Test functionality
gpg --card-status
pcsc_scan
```

#### System Integration
```bash
# Test GPG integration
gpg-connect-agent "scd serialno" /bye
gpg-connect-agent "learn --force" /bye
```

## Troubleshooting

### 1. Common Issues

#### Reset Procedures
```bash
# Reset stuck YubiKey
gpg-connect-agent "scd serialno" "undefined" /bye
gpg-connect-agent reloadagent /bye

# Clear GPG cache
rm -rf ~/.gnupg/private-keys-v1.d/
gpg --card-status
```

#### Error Recovery
```bash
# Fix PIN lockout
ykman piv unblock-pin

# Reset application
ykman openpgp reset
ykman piv reset
```

### 2. Maintenance

#### Firmware Updates
```bash
# Check firmware version
ykman info

# Update firmware (if available)
ykman firmware upgrade
```

#### Health Monitoring
```bash
# Create health check script
cat > check-yubikey-health.sh << EOF
#!/bin/bash

# Check YubiKey presence
if ! ykman list | grep -q "YubiKey"; then
    echo "YubiKey not detected"
    exit 1
fi

# Check GPG status
if ! gpg --card-status > /dev/null 2>&1; then
    echo "GPG card status failed"
    exit 1
fi

# Check PIV application
if ! ykman piv info > /dev/null 2>&1; then
    echo "PIV application not responding"
    exit 1
fi

echo "YubiKey health check passed"
exit 0
EOF

chmod +x check-yubikey-health.sh
``` 