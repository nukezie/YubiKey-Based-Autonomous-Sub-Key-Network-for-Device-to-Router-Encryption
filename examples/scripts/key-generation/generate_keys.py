#!/usr/bin/env python3

"""
YubiKey Key Generation Script
This script automates the generation and management of keys for the YubiKey-Based
Autonomous Sub-Key Network.
"""

import os
import sys
import time
import logging
import argparse
from typing import Dict, List, Optional
import gnupg
import ykman.cli.piv
import ykman.cli.openpgp
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, rsa

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KeyGenerator:
    def __init__(self, config: Dict):
        """Initialize the key generator with configuration."""
        self.config = config
        self.gpg = gnupg.GPG(gnupghome=config['gpg_home'])
        self.yubikey = None
        self.setup_logging()

    def setup_logging(self):
        """Configure detailed logging for key operations."""
        if self.config.get('debug'):
            logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler('key_generation.log')
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)

    def connect_yubikey(self) -> bool:
        """Establish connection with YubiKey."""
        try:
            self.yubikey = ykman.cli.piv.Controller()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to YubiKey: {e}")
            return False

    def generate_master_key(self) -> Optional[str]:
        """Generate master key for the YubiKey network."""
        try:
            # Generate RSA 4096-bit key
            key_params = {
                'Key-Type': 'RSA',
                'Key-Length': 4096,
                'Name-Real': 'YubiKey Network Master',
                'Name-Email': 'master@yubikey-network.local',
                'Expire-Date': 0
            }

            # Generate key
            key_input = self.gpg.gen_key_input(**key_params)
            key = self.gpg.gen_key(key_input)

            if not key:
                raise Exception("Failed to generate master key")

            # Export public key
            public_key = self.gpg.export_keys(key.fingerprint)
            with open('master.pub', 'w') as f:
                f.write(public_key)

            # Generate revocation certificate
            revoke_cert = self.gpg.gen_revoke(
                key.fingerprint,
                "1",  # Compromise
                "Emergency revocation certificate"
            )
            with open('master-revoke.asc', 'w') as f:
                f.write(revoke_cert)

            logger.info(f"Generated master key: {key.fingerprint}")
            return key.fingerprint

        except Exception as e:
            logger.error(f"Failed to generate master key: {e}")
            return None

    def generate_device_subkey(self, master_key: str, device_id: str) -> Optional[str]:
        """Generate a sub-key for a device."""
        try:
            # Generate ECC key for devices
            key_params = {
                'Key-Type': 'ECDSA',
                'Key-Curve': 'nistp256',
                'Key-Usage': 'sign,auth',
                'Name-Real': f'Device {device_id}',
                'Name-Email': f'device-{device_id}@yubikey-network.local',
                'Expire-Date': '1y'
            }

            # Create sub-key
            result = self.gpg.run_command(
                'gpg',
                ['--quick-add-key', master_key, 'nistp256', 'sign', '1y']
            )

            if result.returncode != 0:
                raise Exception(f"Failed to generate sub-key: {result.stderr}")

            subkey_id = result.stdout.strip().split()[-1]
            logger.info(f"Generated device sub-key: {subkey_id}")
            return subkey_id

        except Exception as e:
            logger.error(f"Failed to generate device sub-key: {e}")
            return None

    def generate_router_subkey(self, master_key: str, router_id: str) -> Optional[str]:
        """Generate a sub-key for a router."""
        try:
            # Generate ECC key for routers
            key_params = {
                'Key-Type': 'ECDSA',
                'Key-Curve': 'nistp384',  # Stronger curve for routers
                'Key-Usage': 'sign,auth,encrypt',
                'Name-Real': f'Router {router_id}',
                'Name-Email': f'router-{router_id}@yubikey-network.local',
                'Expire-Date': '6m'
            }

            # Create sub-key
            result = self.gpg.run_command(
                'gpg',
                ['--quick-add-key', master_key, 'nistp384', 'sign', '6m']
            )

            if result.returncode != 0:
                raise Exception(f"Failed to generate sub-key: {result.stderr}")

            subkey_id = result.stdout.strip().split()[-1]
            logger.info(f"Generated router sub-key: {subkey_id}")
            return subkey_id

        except Exception as e:
            logger.error(f"Failed to generate router sub-key: {e}")
            return None

    def import_key_to_yubikey(self, key_id: str, key_type: str) -> bool:
        """Import a key into a YubiKey."""
        try:
            if not self.connect_yubikey():
                raise Exception("No YubiKey connected")

            # Export key for import
            key_data = self.gpg.export_keys(key_id, secret=True)
            
            if key_type == 'device':
                slot = 0x9a  # PIV Authentication
            elif key_type == 'router':
                slot = 0x9c  # PIV Digital Signature
            else:
                raise ValueError(f"Invalid key type: {key_type}")

            # Import to YubiKey
            self.yubikey.import_key(
                slot,
                key_data,
                pin_policy=ykman.cli.piv.PIN_POLICY.ONCE,
                touch_policy=ykman.cli.piv.TOUCH_POLICY.ALWAYS
            )

            logger.info(f"Imported {key_type} key to YubiKey slot {slot:02x}")
            return True

        except Exception as e:
            logger.error(f"Failed to import key to YubiKey: {e}")
            return False

    def verify_key(self, key_id: str) -> bool:
        """Verify a key's integrity and functionality."""
        try:
            # Test signing
            test_data = b"Test message for key verification"
            signature = self.gpg.sign(
                test_data,
                keyid=key_id,
                detach=True
            )

            # Verify signature
            verify = self.gpg.verify_data(
                signature.data,
                test_data
            )

            if not verify:
                raise Exception("Signature verification failed")

            logger.info(f"Successfully verified key: {key_id}")
            return True

        except Exception as e:
            logger.error(f"Key verification failed: {e}")
            return False

    def rotate_key(self, key_id: str) -> Optional[str]:
        """Rotate a key while maintaining its associations."""
        try:
            # Get key info
            key_info = self.gpg.list_keys(keys=[key_id], secret=True)[0]
            
            # Generate new key
            if 'device' in key_info['uids'][0]:
                new_key_id = self.generate_device_subkey(
                    key_info['keyid'],
                    key_info['uids'][0].split()[1]
                )
            elif 'router' in key_info['uids'][0]:
                new_key_id = self.generate_router_subkey(
                    key_info['keyid'],
                    key_info['uids'][0].split()[1]
                )
            else:
                raise ValueError(f"Unknown key type for {key_id}")

            # Revoke old key
            self.gpg.run_command(
                'gpg',
                ['--quick-revoke', key_id]
            )

            logger.info(f"Rotated key {key_id} to {new_key_id}")
            return new_key_id

        except Exception as e:
            logger.error(f"Failed to rotate key: {e}")
            return None

def main():
    """Main function for key generation script."""
    parser = argparse.ArgumentParser(
        description='YubiKey Network Key Generation Tool'
    )
    parser.add_argument(
        '--action',
        choices=['generate-master', 'generate-device', 'generate-router', 'rotate'],
        required=True,
        help='Action to perform'
    )
    parser.add_argument(
        '--id',
        help='ID for device or router key'
    )
    parser.add_argument(
        '--master-key',
        help='Master key ID for sub-key generation'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )

    args = parser.parse_args()

    # Configuration
    config = {
        'gpg_home': os.path.expanduser('~/.gnupg'),
        'debug': args.debug
    }

    generator = KeyGenerator(config)

    try:
        if args.action == 'generate-master':
            key_id = generator.generate_master_key()
            if not key_id:
                sys.exit(1)
            print(f"Generated master key: {key_id}")

        elif args.action == 'generate-device':
            if not args.master_key or not args.id:
                parser.error("--master-key and --id required for device key generation")
            key_id = generator.generate_device_subkey(args.master_key, args.id)
            if not key_id:
                sys.exit(1)
            print(f"Generated device key: {key_id}")

        elif args.action == 'generate-router':
            if not args.master_key or not args.id:
                parser.error("--master-key and --id required for router key generation")
            key_id = generator.generate_router_subkey(args.master_key, args.id)
            if not key_id:
                sys.exit(1)
            print(f"Generated router key: {key_id}")

        elif args.action == 'rotate':
            if not args.id:
                parser.error("--id required for key rotation")
            new_key_id = generator.rotate_key(args.id)
            if not new_key_id:
                sys.exit(1)
            print(f"Rotated key to: {new_key_id}")

    except Exception as e:
        logger.error(f"Operation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()