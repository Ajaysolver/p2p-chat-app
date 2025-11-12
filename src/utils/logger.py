import logging
import logging.handlers
import os
from typing import Dict, Any

def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """Setup logging configuration"""
    log_level = getattr(logging, config.get('level', 'INFO').upper())
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.handlers.RotatingFileHandler(
                'logs/p2p_chat.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
    
    return logging.getLogger(__name__)

def get_logger(name: str) -> logging.Logger:
    """Get logger for a module"""
    return logging.getLogger(name)
