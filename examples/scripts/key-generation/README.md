# YubiKey Network Key Generation Tool

This tool automates the generation and management of keys for the YubiKey-Based Autonomous Sub-Key Network.

## Features

- Master key generation (RSA 4096-bit)
- Device sub-key generation (ECC NIST P-256)
- Router sub-key generation (ECC NIST P-384)
- Key rotation and revocation
- YubiKey import with proper slot assignment
- Key verification and testing

## Prerequisites

- Python 3.8 or higher
- GPG installed and configured
- YubiKey with PIV support
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

## Usage

### Generate Master Key
```bash
python generate_keys.py --action generate-master
```

### Generate Device Key
```bash
python generate_keys.py --action generate-device --master-key <master-key-id> --id <device-id>
```

### Generate Router Key
```bash
python generate_keys.py --action generate-router --master-key <master-key-id> --id <router-id>
```

### Rotate Key
```bash
python generate_keys.py --action rotate --id <key-id>
```

### Enable Debug Logging
Add `--debug` flag to any command to enable detailed logging:
```bash
python generate_keys.py --action generate-master --debug
```

## Key Types and Specifications

### Master Key
- Algorithm: RSA 4096-bit
- Usage: Key signing, certification
- Expiration: Never expires
- Storage: Offline, secure storage recommended

### Device Sub-keys
- Algorithm: ECDSA with NIST P-256
- Usage: Authentication, signing
- Expiration: 1 year
- YubiKey Slot: PIV Authentication (0x9A)

### Router Sub-keys
- Algorithm: ECDSA with NIST P-384
- Usage: Authentication, signing, encryption
- Expiration: 6 months
- YubiKey Slot: PIV Digital Signature (0x9C)

## Security Considerations

1. **Master Key Protection**
   - Keep the master key offline
   - Store revocation certificate securely
   - Use strong passphrases

2. **YubiKey Configuration**
   - PIN protection enabled
   - Touch policy enforced for key operations
   - Regular key rotation

3. **Key Management**
   - Regular verification of key integrity
   - Proper handling of revoked keys
   - Secure backup procedures

## Logging

- Default log level: INFO
- Debug logging available with --debug flag
- Log file: key_generation.log (when debug enabled)

## Error Handling

The script includes comprehensive error handling:
- Connection failures
- Key generation errors
- YubiKey operations
- Verification failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.