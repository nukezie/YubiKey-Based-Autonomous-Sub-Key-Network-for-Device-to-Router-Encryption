#!/usr/bin/env python3

"""
YubiKey Network Backup Script
This script implements automated backup and recovery procedures for the
YubiKey-Based Autonomous Sub-Key Network.
"""

import os
import sys
import time
import logging
import argparse
import shutil
import tarfile
import json
import yaml
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import gnupg
import psycopg2
import redis
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BackupManager:
    """Manages backup operations for the YubiKey network."""
    
    def __init__(self, config: Dict):
        """Initialize backup manager with configuration."""
        self.config = config
        self.backup_path = config['backup']['path']
        self.gpg = gnupg.GPG(gnupghome=config['gpg_home'])
        self.setup_logging()
        self.setup_encryption()
        
    def setup_logging(self):
        """Configure logging based on configuration."""
        if self.config.get('debug'):
            logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler('backup.log')
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            
    def setup_encryption(self):
        """Set up encryption for backups."""
        try:
            if self.config['backup']['encrypt_backups']:
                key = Fernet.generate_key()
                with open(self.config['backup']['key_file'], 'wb') as f:
                    f.write(key)
                self.fernet = Fernet(key)
            else:
                self.fernet = None
        except Exception as e:
            logger.error(f"Failed to setup encryption: {e}")
            sys.exit(1)
            
    def create_backup(self) -> bool:
        """Create a complete backup of the YubiKey network."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join(self.backup_path, timestamp)
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup components
            success = all([
                self.backup_keys(backup_dir),
                self.backup_config(backup_dir),
                self.backup_database(backup_dir),
                self.backup_state(backup_dir)
            ])
            
            if success:
                # Create archive
                archive_path = self.create_archive(backup_dir, timestamp)
                
                # Encrypt if configured
                if self.fernet:
                    self.encrypt_backup(archive_path)
                    
                # Cleanup temporary files
                shutil.rmtree(backup_dir)
                
                logger.info(f"Backup completed successfully: {archive_path}")
                return True
            else:
                logger.error("Backup failed")
                return False
                
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
            
    def backup_keys(self, backup_dir: str) -> bool:
        """Backup YubiKey-related keys and certificates."""
        try:
            keys_dir = os.path.join(backup_dir, 'keys')
            os.makedirs(keys_dir, exist_ok=True)
            
            # Export GPG keys
            public_keys = self.gpg.export_keys(self.config['backup']['key_ids'])
            secret_keys = self.gpg.export_keys(
                self.config['backup']['key_ids'],
                secret=True
            )
            
            with open(os.path.join(keys_dir, 'public_keys.asc'), 'w') as f:
                f.write(public_keys)
            with open(os.path.join(keys_dir, 'secret_keys.asc'), 'w') as f:
                f.write(secret_keys)
                
            # Backup certificates
            cert_src = self.config['ssl']['cert_path']
            key_src = self.config['ssl']['key_path']
            shutil.copy2(cert_src, os.path.join(keys_dir, 'server.crt'))
            shutil.copy2(key_src, os.path.join(keys_dir, 'server.key'))
            
            logger.info("Keys backup completed")
            return True
            
        except Exception as e:
            logger.error(f"Keys backup failed: {e}")
            return False
            
    def backup_config(self, backup_dir: str) -> bool:
        """Backup configuration files."""
        try:
            config_dir = os.path.join(backup_dir, 'config')
            os.makedirs(config_dir, exist_ok=True)
            
            # Backup main configuration
            config_src = self.config['paths']['config_dir']
            for file in os.listdir(config_src):
                if file.endswith('.conf') or file.endswith('.yml'):
                    src_path = os.path.join(config_src, file)
                    dst_path = os.path.join(config_dir, file)
                    shutil.copy2(src_path, dst_path)
                    
            logger.info("Configuration backup completed")
            return True
            
        except Exception as e:
            logger.error(f"Configuration backup failed: {e}")
            return False
            
    def backup_database(self, backup_dir: str) -> bool:
        """Backup PostgreSQL database."""
        try:
            db_dir = os.path.join(backup_dir, 'database')
            os.makedirs(db_dir, exist_ok=True)
            
            # Connect to database
            conn = psycopg2.connect(
                host=self.config['database']['host'],
                port=self.config['database']['port'],
                dbname=self.config['database']['name'],
                user=self.config['database']['user']
            )
            
            # Create SQL dump
            with conn.cursor() as cur:
                with open(os.path.join(db_dir, 'backup.sql'), 'w') as f:
                    cur.copy_expert(f"COPY (SELECT * FROM pg_catalog.pg_tables) TO STDOUT", f)
                    
            conn.close()
            logger.info("Database backup completed")
            return True
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            return False
            
    def backup_state(self, backup_dir: str) -> bool:
        """Backup system state and Redis data."""
        try:
            state_dir = os.path.join(backup_dir, 'state')
            os.makedirs(state_dir, exist_ok=True)
            
            # Connect to Redis
            r = redis.Redis(
                host=self.config['redis']['host'],
                port=self.config['redis']['port'],
                db=self.config['redis']['db']
            )
            
            # Backup Redis data
            data = {}
            for key in r.keys('*'):
                key_str = key.decode('utf-8')
                value = r.get(key)
                if value:
                    data[key_str] = value.decode('utf-8')
                    
            with open(os.path.join(state_dir, 'redis_dump.json'), 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info("State backup completed")
            return True
            
        except Exception as e:
            logger.error(f"State backup failed: {e}")
            return False
            
    def create_archive(self, backup_dir: str, timestamp: str) -> str:
        """Create compressed archive of backup directory."""
        try:
            archive_name = f"yubikey_backup_{timestamp}.tar.gz"
            archive_path = os.path.join(self.backup_path, archive_name)
            
            with tarfile.open(archive_path, "w:gz") as tar:
                tar.add(backup_dir, arcname=os.path.basename(backup_dir))
                
            logger.info(f"Created backup archive: {archive_path}")
            return archive_path
            
        except Exception as e:
            logger.error(f"Archive creation failed: {e}")
            return ""
            
    def encrypt_backup(self, archive_path: str):
        """Encrypt backup archive."""
        try:
            with open(archive_path, 'rb') as f:
                data = f.read()
                
            encrypted_data = self.fernet.encrypt(data)
            
            with open(f"{archive_path}.enc", 'wb') as f:
                f.write(encrypted_data)
                
            os.remove(archive_path)
            logger.info("Backup encryption completed")
            
        except Exception as e:
            logger.error(f"Backup encryption failed: {e}")
            
    def restore_backup(self, backup_path: str) -> bool:
        """Restore system from backup."""
        try:
            # Decrypt if necessary
            if backup_path.endswith('.enc'):
                backup_path = self.decrypt_backup(backup_path)
                
            # Extract archive
            temp_dir = os.path.join(self.backup_path, 'temp_restore')
            os.makedirs(temp_dir, exist_ok=True)
            
            with tarfile.open(backup_path, "r:gz") as tar:
                tar.extractall(temp_dir)
                
            # Restore components
            success = all([
                self.restore_keys(temp_dir),
                self.restore_config(temp_dir),
                self.restore_database(temp_dir),
                self.restore_state(temp_dir)
            ])
            
            # Cleanup
            shutil.rmtree(temp_dir)
            
            if success:
                logger.info("Restore completed successfully")
                return True
            else:
                logger.error("Restore failed")
                return False
                
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False
            
    def decrypt_backup(self, encrypted_path: str) -> str:
        """Decrypt encrypted backup file."""
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
                
            decrypted_data = self.fernet.decrypt(encrypted_data)
            decrypted_path = encrypted_path[:-4]  # Remove .enc
            
            with open(decrypted_path, 'wb') as f:
                f.write(decrypted_data)
                
            logger.info("Backup decryption completed")
            return decrypted_path
            
        except Exception as e:
            logger.error(f"Backup decryption failed: {e}")
            return ""

def main():
    """Main function for the backup script."""
    parser = argparse.ArgumentParser(
        description='YubiKey Network Backup Tool'
    )
    parser.add_argument(
        '--config',
        required=True,
        help='Path to configuration file'
    )
    parser.add_argument(
        '--action',
        choices=['backup', 'restore'],
        required=True,
        help='Action to perform'
    )
    parser.add_argument(
        '--backup-path',
        help='Path to backup file (required for restore)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
            
        # Add debug flag to config
        config['debug'] = args.debug
        
        # Create backup manager
        manager = BackupManager(config)
        
        if args.action == 'backup':
            success = manager.create_backup()
        elif args.action == 'restore':
            if not args.backup_path:
                parser.error("--backup-path required for restore action")
            success = manager.restore_backup(args.backup_path)
            
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 