import socket
import threading
import time
import json
from typing import List, Dict, Any

# Absolute imports from src package
from src.security.encryption import EncryptionManager
from src.network.protocol import MessageProtocol
from src.core.connection_manager import ConnectionManager
from src.core.peer_discovery import PeerDiscovery
from src.utils.logger import get_logger

class P2PNode:
    def __init__(self, host: str, port: int, config: Dict[str, Any]):
        self.host = host
        self.port = port
        self.config = config
        self.logger = get_logger(__name__)
        
        # Initialize components
        self.encryption_manager = EncryptionManager(config.get('security', {}))
        self.protocol = MessageProtocol()
        self.connection_manager = ConnectionManager(self)
        self.peer_discovery = PeerDiscovery(self, config)
        
        self.running = False
        self.server_socket = None
        self.peers = {}  # peer_id -> connection_info
        self.message_handler = None  # Will be set by UI
        
    def start(self):
        """Start the P2P node"""
        self.running = True
        
        # Generate node keys
        self.encryption_manager.generate_keys()
        
        # Start server
        self._start_server()
        
        # Start peer discovery
        self.peer_discovery.start()
        
        self.logger.info(f"P2P Node started on {self.host}:{self.port}")
        
    def _start_server(self):
        """Start listening for incoming connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        
        server_thread = threading.Thread(target=self._accept_connections)
        server_thread.daemon = True
        server_thread.start()
    
    def _accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                self.logger.info(f"New connection from {addr}")
                
                # Handle connection in new thread
                connection_thread = threading.Thread(
                    target=self.connection_manager.handle_incoming_connection,
                    args=(client_socket, addr)
                )
                connection_thread.daemon = True
                connection_thread.start()
                
            except Exception as e:
                if self.running:
                    self.logger.error(f"Error accepting connection: {e}")
    
    def connect_to_peer(self, host: str, port: int) -> bool:
        """Connect to a peer"""
        return self.connection_manager.connect_to_peer(host, port)
    
    def send_message(self, message: str, peer_id: str = None):
        """Send message to specific peer or broadcast to all"""
        if peer_id:
            self.connection_manager.send_to_peer(peer_id, message)
        else:
            self.connection_manager.broadcast_message(message)
    
    def stop(self):
        """Stop the P2P node"""
        self.running = False
        self.peer_discovery.stop()
        self.connection_manager.close_all_connections()
        
        if self.server_socket:
            self.server_socket.close()
        
        self.logger.info("P2P Node stopped")
