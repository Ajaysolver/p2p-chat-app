import cmd
import threading
import time

# Absolute imports from src package
from src.core.message_handler import MessageHandler
from src.utils.logger import get_logger

class CLIInterface(cmd.Cmd):
    prompt = 'p2p-chat> '
    
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.logger = get_logger(__name__)
        self.messages = []
        self.running = True
        
        # Initialize message handler in node
        self.node.message_handler = MessageHandler(node, node.encryption_manager)
        self._setup_message_handlers()
        
    def _setup_message_handlers(self):
        """Setup message handlers"""
        self.node.message_handler.register_callback('chat_message', self._handle_chat_message)
    
    def _handle_chat_message(self, payload, peer_id):
        """Handle incoming chat messages"""
        message_text = f"{peer_id}: {payload.get('text', '')}"
        self.messages.append(message_text)
    
    def run(self):
        """Start the CLI interface"""
        print("P2P Secure Chat Application")
        print("Type 'help' for commands")
        
        # Start message display thread
        display_thread = threading.Thread(target=self._display_messages)
        display_thread.daemon = True
        display_thread.start()
        
        self.cmdloop()
    
    def _display_messages(self):
        """Background thread to display new messages"""
        last_count = 0
        while self.running:
            if len(self.messages) > last_count:
                for i in range(last_count, len(self.messages)):
                    print(f"\n{self.messages[i]}\n{self.prompt}", end='', flush=True)
                last_count = len(self.messages)
            time.sleep(0.1)
    
    def do_connect(self, arg):
        """Connect to a peer: connect <host> <port>"""
        try:
            host, port = arg.split()
            success = self.node.connect_to_peer(host, int(port))
            if success:
                print(f"Connected to {host}:{port}")
            else:
                print(f"Failed to connect to {host}:{port}")
        except ValueError:
            print("Usage: connect <host> <port>")
    
    def do_send(self, arg):
        """Send a message: send <message>"""
        if arg:
            # Create formatted message
            message = self.node.message_handler.create_chat_message(arg)
            self.node.send_message(message)
            self.messages.append(f"You: {arg}")
        else:
            print("Usage: send <message>")
    
    def do_peers(self, arg):
        """List connected peers"""
        peers = self.node.connection_manager.get_connected_peers()
        if peers:
            print("Connected peers:")
            for peer_id, info in peers.items():
                print(f"  {peer_id} - {info['address']}")
        else:
            print("No connected peers")
    
    def do_quit(self, arg):
        """Exit the application"""
        print("Goodbye!")
        self.running = False
        self.node.stop()
        return True
    
    def do_clear(self, arg):
        """Clear the screen"""
        import os
        os.system('clear')
    
    def postcmd(self, stop, line):
        return stop
