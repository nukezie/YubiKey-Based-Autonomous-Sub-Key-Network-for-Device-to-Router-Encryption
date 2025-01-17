#!/usr/bin/env python3

"""
YubiKey Network Deployment Script
This script automates the deployment and setup of the YubiKey-Based
Autonomous Sub-Key Network.
"""

import os
import sys
import time
import logging
import argparse
import subprocess
import shutil
import yaml
from typing import Dict, List, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NetworkDeployer:
    """Manages deployment of the YubiKey network."""
    
    def __init__(self, config: Dict):
        """Initialize deployer with configuration."""
        self.config = config
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging based on configuration."""
        if self.config.get('debug'):
            logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler('deployment.log')
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
            
    def deploy(self) -> bool:
        """Deploy the complete YubiKey network."""
        try:
            success = all([
                self.check_prerequisites(),
                self.setup_directories(),
                self.install_dependencies(),
                self.configure_system(),
                self.setup_database(),
                self.setup_redis(),
                self.configure_ssl(),
                self.setup_yubikey(),
                self.configure_services(),
                self.start_services()
            ])
            
            if success:
                logger.info("Deployment completed successfully")
                return True
            else:
                logger.error("Deployment failed")
                return False
                
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            return False
            
    def check_prerequisites(self) -> bool:
        """Check system prerequisites."""
        try:
            # Check Python version
            python_version = sys.version_info
            if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
                raise Exception("Python 3.8 or higher required")
                
            # Check required system packages
            required_packages = [
                'postgresql',
                'redis-server',
                'nginx',
                'supervisor',
                'gpg'
            ]
            
            for package in required_packages:
                result = subprocess.run(['which', package], capture_output=True)
                if result.returncode != 0:
                    raise Exception(f"Required package not found: {package}")
                    
            logger.info("Prerequisites check passed")
            return True
            
        except Exception as e:
            logger.error(f"Prerequisites check failed: {e}")
            return False
            
    def setup_directories(self) -> bool:
        """Create required directories."""
        try:
            directories = [
                self.config['paths']['config_dir'],
                self.config['paths']['data_dir'],
                self.config['paths']['log_dir'],
                self.config['paths']['backup_dir'],
                self.config['paths']['ssl_dir']
            ]
            
            for directory in directories:
                os.makedirs(directory, exist_ok=True)
                # Set proper permissions
                os.chmod(directory, 0o750)
                
            logger.info("Directory setup completed")
            return True
            
        except Exception as e:
            logger.error(f"Directory setup failed: {e}")
            return False
            
    def install_dependencies(self) -> bool:
        """Install Python dependencies."""
        try:
            # Create virtual environment
            venv_path = self.config['paths']['venv_dir']
            subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
            
            # Install requirements
            pip_path = os.path.join(venv_path, 'bin', 'pip')
            requirements_file = os.path.join(
                self.config['paths']['config_dir'],
                'requirements.txt'
            )
            subprocess.run([pip_path, 'install', '-r', requirements_file], check=True)
            
            logger.info("Dependencies installation completed")
            return True
            
        except Exception as e:
            logger.error(f"Dependencies installation failed: {e}")
            return False
            
    def configure_system(self) -> bool:
        """Configure system settings."""
        try:
            # Copy configuration files
            config_files = {
                'server.conf': '/etc/yubikey-network/server.conf',
                'gpg-agent.conf': '~/.gnupg/gpg-agent.conf',
                'supervisord.conf': '/etc/supervisor/conf.d/yubikey-network.conf',
                'nginx.conf': '/etc/nginx/sites-available/yubikey-network'
            }
            
            for src, dst in config_files.items():
                src_path = os.path.join(self.config['paths']['config_src'], src)
                dst_path = os.path.expanduser(dst)
                shutil.copy2(src_path, dst_path)
                
            # Enable nginx site
            nginx_link = '/etc/nginx/sites-enabled/yubikey-network'
            if not os.path.exists(nginx_link):
                os.symlink(
                    '/etc/nginx/sites-available/yubikey-network',
                    nginx_link
                )
                
            logger.info("System configuration completed")
            return True
            
        except Exception as e:
            logger.error(f"System configuration failed: {e}")
            return False
            
    def setup_database(self) -> bool:
        """Set up PostgreSQL database."""
        try:
            # Create database and user
            commands = [
                f"createuser -s {self.config['database']['user']}",
                f"createdb -O {self.config['database']['user']} {self.config['database']['name']}"
            ]
            
            for cmd in commands:
                subprocess.run(['sudo', '-u', 'postgres', 'psql', '-c', cmd], check=True)
                
            # Apply schema
            schema_file = os.path.join(
                self.config['paths']['config_src'],
                'schema.sql'
            )
            subprocess.run([
                'psql',
                '-U', self.config['database']['user'],
                '-d', self.config['database']['name'],
                '-f', schema_file
            ], check=True)
            
            logger.info("Database setup completed")
            return True
            
        except Exception as e:
            logger.error(f"Database setup failed: {e}")
            return False
            
    def setup_redis(self) -> bool:
        """Set up Redis server."""
        try:
            # Configure Redis
            redis_conf = '/etc/redis/redis.conf'
            with open(redis_conf, 'a') as f:
                f.write(f"\nport {self.config['redis']['port']}\n")
                f.write(f"bind {self.config['redis']['bind']}\n")
                f.write(f"maxmemory {self.config['redis']['maxmemory']}\n")
                f.write(f"maxmemory-policy {self.config['redis']['maxmemory_policy']}\n")
                
            # Restart Redis
            subprocess.run(['systemctl', 'restart', 'redis'], check=True)
            
            logger.info("Redis setup completed")
            return True
            
        except Exception as e:
            logger.error(f"Redis setup failed: {e}")
            return False
            
    def configure_ssl(self) -> bool:
        """Configure SSL certificates."""
        try:
            cert_path = self.config['ssl']['cert_path']
            key_path = self.config['ssl']['key_path']
            
            # Generate self-signed certificate if not exists
            if not (os.path.exists(cert_path) and os.path.exists(key_path)):
                subprocess.run([
                    'openssl', 'req', '-x509', '-nodes',
                    '-days', '365',
                    '-newkey', 'rsa:2048',
                    '-keyout', key_path,
                    '-out', cert_path,
                    '-subj', '/CN=yubikey-network'
                ], check=True)
                
            logger.info("SSL configuration completed")
            return True
            
        except Exception as e:
            logger.error(f"SSL configuration failed: {e}")
            return False
            
    def setup_yubikey(self) -> bool:
        """Configure YubiKey settings."""
        try:
            # Initialize YubiKey configuration
            subprocess.run([
                'ykman', 'piv', 'reset', '-f'
            ], check=True)
            
            # Set PIN and PUK
            subprocess.run([
                'ykman', 'piv', 'access', 'change-pin',
                '-P', '123456',
                '-n', self.config['yubikey']['pin']
            ], check=True)
            
            subprocess.run([
                'ykman', 'piv', 'access', 'change-puk',
                '-p', '12345678',
                '-n', self.config['yubikey']['puk']
            ], check=True)
            
            logger.info("YubiKey setup completed")
            return True
            
        except Exception as e:
            logger.error(f"YubiKey setup failed: {e}")
            return False
            
    def configure_services(self) -> bool:
        """Configure system services."""
        try:
            services = [
                'yubikey-network.service',
                'yubikey-monitor.service'
            ]
            
            for service in services:
                src = os.path.join(self.config['paths']['config_src'], service)
                dst = f"/etc/systemd/system/{service}"
                shutil.copy2(src, dst)
                
                # Reload and enable service
                subprocess.run(['systemctl', 'daemon-reload'], check=True)
                subprocess.run(['systemctl', 'enable', service], check=True)
                
            logger.info("Services configuration completed")
            return True
            
        except Exception as e:
            logger.error(f"Services configuration failed: {e}")
            return False
            
    def start_services(self) -> bool:
        """Start all services."""
        try:
            services = [
                'nginx',
                'redis-server',
                'postgresql',
                'supervisor',
                'yubikey-network',
                'yubikey-monitor'
            ]
            
            for service in services:
                subprocess.run(['systemctl', 'restart', service], check=True)
                
            logger.info("Services started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start services: {e}")
            return False

def main():
    """Main function for the deployment script."""
    parser = argparse.ArgumentParser(
        description='YubiKey Network Deployment Tool'
    )
    parser.add_argument(
        '--config',
        required=True,
        help='Path to deployment configuration file'
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
        
        # Create deployer and run deployment
        deployer = NetworkDeployer(config)
        success = deployer.deploy()
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 