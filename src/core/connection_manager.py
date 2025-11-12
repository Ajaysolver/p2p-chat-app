import socket
import threading
import json
import time
from typing import Dict, Any

# Absolute imports from src package
from src.utils.logger import get_logger

class ConnectionManager:
    def __init__(self, node):
        self.node = node
        self.logger = get_logger(__name__)
        self.connections = {}  # peer_id -> socket
        self.connection_lock = threading.Lock()
        
    def handle_incoming_connection(self, client_socket, addr):
        """Handle incoming connection"""
        peer_id = f"{addr[0]}:{addr[1]}"
        
        with self.connection_lock:
            self.connections[peer_id] = client_socket
        
        self.logger.info(f"Connection established with {peer_id}")
        
        try:
            while self.node.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                    
                # Handle received message
                message = data.decode('utf-8')
                self.node.message_handler.handle_message(message, peer_id)
                
        except Exception as e:
            self.logger.error(f"Connection error with {peer_id}: {e}")
        finally:
            self._remove_connection(peer_id)
            client_socket.close()
    
    def connect_to_peer(self, host: str, port: int) -> bool:
        """Connect to a peer"""
        peer_id = f"{host}:{port}"
        
        if peer_id in self.connections:
            self.logger.info(f"Already connected to {peer_id}")
            return True
            
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, port))
            
            with self.connection_lock:
                self.connections[peer_id] = sock
            
            # Start thread to listen to this peer
            listen_thread = threading.Thread(
                target=self._listen_to_peer,
                args=(sock, peer_id)
            )
            listen_thread.daemon = True
            listen_thread.start()
            
            self.logger.info(f"Connected to {peer_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to {peer_id}: {e}")
            return False
    
    def _listen_to_peer(self, sock, peer_id):
        """Listen to messages from a peer"""
        try:
            while self.node.running:
                data = sock.recv(4096)
                if not data:
                    break
                    
                message = data.decode('utf-8')
                self.node.message_handler.handle_message(message, peer_id)
                
        except Exception as e:
            self.logger.debug(f"Listening to {peer_id} ended: {e}")
        finally:
            self._remove_connection(peer_id)
    
    def send_to_peer(self, peer_id: str, message: str):
        """Send message to specific peer"""
        with self.connection_lock:
            if peer_id in self.connections:
                try:
                    sock = self.connections[peer_id]
                    sock.send(message.encode('utf-8'))
                except Exception as e:
                    self.logger.error(f"Failed to send to {peer_id}: {e}")
                    self._remove_connection(peer_id)
    
    def broadcast_message(self, message: str):
        """Broadcast message to all connected peers"""
        with self.connection_lock:
            disconnected_peers = []
            for peer_id, sock in self.connections.items():
                try:
                    sock.send(message.encode('utf-8'))
                except Exception as e:
                    self.logger.error(f"Failed to send to {peer_id}: {e}")
                    disconnected_peers.append(peer_id)
            
            # Remove disconnected peers
            for peer_id in disconnected_peers:
                self._remove_connection(peer_id)
    
    def _remove_connection(self, peer_id: str):
        """Remove a connection"""
        with self.connection_lock:
            if peer_id in self.connections:
                try:
                    self.connections[peer_id].close()
                except:
                    pass
                del self.connections[peer_id]
                self.logger.info(f"Connection to {peer_id} closed")
    
    def close_all_connections(self):
        """Close all connections"""
        with self.connection_lock:
            for peer_id, sock in self.connections.items():
                try:
                    sock.close()
                except:
                    pass
            self.connections.clear()
    
    def get_connected_peers(self) -> Dict[str, Any]:
        """Get list of connected peers"""
        with self.connection_lock:
            return {peer_id: {'address': peer_id} for peer_id in self.connections.keys()}
