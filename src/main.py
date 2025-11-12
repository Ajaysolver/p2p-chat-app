#!/usr/bin/env python3
import argparse
import sys
import os
import signal

# Absolute imports from src package
from src.core.p2p_node import P2PNode
from src.ui.cli_interface import CLIInterface
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logging

class P2PChatApplication:
    def __init__(self):
        self.node = None
        self.interface = None
        self.logger = None
        
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(sig, frame):
            print("\nReceived shutdown signal...")
            self.shutdown()
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def shutdown(self):
        """Graceful shutdown"""
        if self.node:
            self.node.stop()
        if self.interface:
            # For GUI, we need to properly close the window
            if hasattr(self.interface, 'root') and self.interface.root:
                self.interface.root.quit()
        sys.exit(0)
    
    def run(self, args):
        """Main application entry point"""
        # Load configuration
        config = ConfigLoader.load_config(args.config)
        
        # Setup logging
        self.logger = setup_logging(config.get('logging', {}))
        
        try:
            # Create P2P node
            self.node = P2PNode(
                host=args.host,
                port=args.port,
                config=config
            )
            
            # Setup signal handlers
            self.setup_signal_handlers()
            
            # Start the node
            self.node.start()
            
            # Start interface
            if args.gui:
                try:
                    from src.ui.gui_interface import GUIInterface
                    self.interface = GUIInterface(self.node)
                    print(f"Starting GUI interface on {args.host}:{args.port}")
                    self.interface.run()
                except ImportError as e:
                    print(f"GUI failed to load: {e}. Falling back to CLI.")
                    self.interface = CLIInterface(self.node)
                    self.interface.run()
            else:
                self.interface = CLIInterface(self.node)
                self.interface.run()
                
        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            if self.logger:
                self.logger.exception("Detailed error:")
            sys.exit(1)
        finally:
            self.shutdown()

def main():
    parser = argparse.ArgumentParser(
        description='P2P Secure Chat Application - Kali Linux',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python run.py --port 5000 --gui
  python run.py --port 5001 --host 0.0.0.0
  python run.py --port 5002 --bootstrap localhost:5000
        '''
    )
    parser.add_argument('--port', type=int, default=5000, 
                       help='Port to listen on (default: 5000)')
    parser.add_argument('--host', default='localhost', 
                       help='Host to bind to (default: localhost)')
    parser.add_argument('--bootstrap', 
                       help='Bootstrap node address (host:port)')
    parser.add_argument('--config', default='config/default_config.json', 
                       help='Config file path (default: config/default_config.json)')
    parser.add_argument('--gui', action='store_true', 
                       help='Use GUI interface (default: CLI)')
    
    args = parser.parse_args()
    
    app = P2PChatApplication()
    app.run(args)

if __name__ == "__main__":
    main()
