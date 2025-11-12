import hashlib
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from ..utils.logger import get_logger

class KeyExchange:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.private_key = None
        self.public_key = None
        self.shared_secret = None
        
    def generate_ec_keys(self):
        """Generate Elliptic Curve keys for ECDH"""
        self.private_key = ec.generate_private_key(ec.SECP384R1())
        self.public_key = self.private_key.public_key()
        
    def get_public_key_bytes(self) -> bytes:
        """Get public key as bytes"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
    def derive_shared_secret(self, peer_public_key_pem: bytes) -> bytes:
        """Derive shared secret using ECDH"""
        try:
            # Load peer public key
            peer_public_key = serialization.load_pem_public_key(peer_public_key_pem)
            
            # Perform key exchange
            self.shared_secret = self.private_key.exchange(ec.ECDH(), peer_public_key)
            
            # Derive encryption key using HKDF
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'p2p-chat-key',
            ).derive(self.shared_secret)
            
            return derived_key
            
        except Exception as e:
            self.logger.error(f"Key exchange failed: {e}")
            raise
