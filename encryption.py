from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import base64
import os
import json
from typing import Dict, Any

class EncryptionManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.private_key = None
        self.public_key = None
        self.symmetric_key = None
        self.fernet = None
        
    def generate_keys(self):
        """Generate RSA key pair"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        
    def derive_symmetric_key(self, password: str, salt: bytes = None):
        """Derive symmetric key from password"""
        if salt is None:
            salt = os.urandom(16)
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.symmetric_key = key
        self.fernet = Fernet(key)
        return salt
    
    def encrypt_message(self, message: str) -> str:
        """Encrypt message using symmetric encryption"""
        if not self.fernet:
            raise Exception("Symmetric key not set")
        return self.fernet.encrypt(message.encode()).decode()
    
    def decrypt_message(self, encrypted_message: str) -> str:
        """Decrypt message using symmetric encryption"""
        if not self.fernet:
            raise Exception("Symmetric key not set")
        return self.fernet.decrypt(encrypted_message.encode()).decode()
    
    def get_public_key_pem(self) -> str:
        """Get public key in PEM format"""
        if not self.public_key:
            raise Exception("Public key not generated")
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
