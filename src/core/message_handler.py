import json
import time
from typing import Dict, Any

# Absolute imports from src package
from src.security.encryption import EncryptionManager
from src.utils.logger import get_logger

class MessageHandler:
    def __init__(self, node, encryption_manager: EncryptionManager):
        self.node = node
        self.encryption_manager = encryption_manager
        self.logger = get_logger(__name__)
        self.message_callbacks = {}
        
    def register_callback(self, message_type: str, callback):
        """Register callback for specific message type"""
        self.message_callbacks[message_type] = callback
    
    def handle_message(self, raw_data: str, peer_id: str):
        """Handle incoming message"""
        try:
            # Parse message
            message = json.loads(raw_data)
            message_type = message.get('type')
            payload = message.get('payload', {})
            
            # Call registered callback
            if message_type in self.message_callbacks:
                self.message_callbacks[message_type](payload, peer_id)
            else:
                self.logger.warning(f"No handler for message type: {message_type}")
                
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON message")
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
    
    def create_chat_message(self, text: str) -> str:
        """Create a chat message"""
        message = {
            'type': 'chat_message',
            'payload': {
                'text': text,
                'timestamp': time.time(),
                'sender': self.node.port  # Using port as identifier for demo
            }
        }
        return json.dumps(message)
