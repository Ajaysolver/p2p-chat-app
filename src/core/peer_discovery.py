import threading
import time
import socket
import json
from typing import List

# Absolute imports from src package
from src.utils.logger import get_logger

class PeerDiscovery:
    def __init__(self, node, config):
        self.node = node
        self.config = config
        self.logger = get_logger(__name__)
        self.running = False
        self.discovery_thread = None
        self.bootstrap_nodes = config.get('network', {}).get('bootstrap_nodes', [])
        
    def start(self):
        """Start peer discovery"""
        self.running = True
        self.discovery_thread = threading.Thread(target=self._discovery_loop)
        self.discovery_thread.daemon = True
        self.discovery_thread.start()
        self.logger.info("Peer discovery started")
        
    def stop(self):
        """Stop peer discovery"""
        self.running = False
        if self.discovery_thread:
            self.discovery_thread.join(timeout=5)
        self.logger.info("Peer discovery stopped")
    
    def _discovery_loop(self):
        """Main discovery loop"""
        while self.running:
            try:
                self._discover_peers()
                time.sleep(30)  # Discover peers every 30 seconds
            except Exception as e:
                self.logger.error(f"Discovery error: {e}")
                time.sleep(10)
    
    def _discover_peers(self):
        """Discover peers from bootstrap nodes"""
        for bootstrap_node in self.bootstrap_nodes:
            try:
                host, port = bootstrap_node.split(':')
                self._connect_to_bootstrap(host, int(port))
            except Exception as e:
                self.logger.debug(f"Failed to connect to bootstrap {bootstrap_node}: {e}")
    
    def _connect_to_bootstrap(self, host: str, port: int):
        """Connect to bootstrap node and get peer list"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((host, port))
            
            # Send registration message
            message = {
                'type': 'register',
                'payload': {
                    'host': self.node.host,
                    'port': self.node.port
                }
            }
            sock.send(json.dumps(message).encode())
            
            # Receive peer list
            response = sock.recv(4096).decode()
            peer_list = json.loads(response)
            
            # Connect to peers
            for peer_info in peer_list:
                if peer_info['host'] != self.node.host or peer_info['port'] != self.node.port:
                    self.node.connect_to_peer(peer_info['host'], peer_info['port'])
                    
            sock.close()
            
        except Exception as e:
            self.logger.debug(f"Bootstrap connection failed: {e}")
