import json
import struct
from typing import Dict, Any

class MessageProtocol:
    def __init__(self):
        self.header_format = '!I'  # 4-byte message length
    
    def create_message(self, message_type: str, payload: Dict[str, Any]) -> bytes:
        """Create a message with header"""
        message_data = json.dumps({
            'type': message_type,
            'payload': payload
        }).encode('utf-8')
        
        # Add length header
        header = struct.pack(self.header_format, len(message_data))
        return header + message_data
    
    def parse_message(self, data: bytes) -> Dict[str, Any]:
        """Parse message from bytes"""
        try:
            return json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
    
    def get_message_length(self, header: bytes) -> int:
        """Get message length from header"""
        return struct.unpack(self.header_format, header)[0]
