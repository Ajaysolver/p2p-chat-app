import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from typing import Dict, List

# Absolute imports from src package
from src.core.message_handler import MessageHandler
from src.utils.logger import get_logger

class GUIInterface:
    def __init__(self, node):
        self.node = node
        self.logger = get_logger(__name__)
        self.root = None
        self.connected_peers = {}
        
        # Initialize message handler
        self.node.message_handler = MessageHandler(node, node.encryption_manager)
        self._setup_message_handlers()
    
    def _setup_message_handlers(self):
        """Setup message handlers for GUI"""
        self.node.message_handler.register_callback('chat_message', self._handle_chat_message)
        self.node.message_handler.register_callback('peer_list', self._handle_peer_list)
    
    def _handle_chat_message(self, payload, peer_id):
        """Handle incoming chat messages for GUI"""
        if self.root:
            timestamp = time.strftime("%H:%M:%S", time.localtime(payload.get('timestamp', time.time())))
            message = f"[{timestamp}] {peer_id}: {payload.get('text', '')}"
            self._update_chat_display(message)
    
    def _handle_peer_list(self, payload, peer_id):
        """Handle peer list updates"""
        if self.root:
            self.connected_peers = payload.get('peers', {})
            self._update_peer_list()
    
    def run(self):
        """Start the GUI interface"""
        self.root = tk.Tk()
        self._setup_gui()
        self.root.mainloop()
    
    def _setup_gui(self):
        """Setup the main GUI window"""
        self.root.title("P2P Secure Chat - Kali Linux")
        self.root.geometry("900x600")
        self.root.configure(bg='#2b2b2b')
        
        # Configure styles
        self._configure_styles()
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel (chat area)
        self._create_chat_area(main_frame)
        
        # Create right panel (peers and controls)
        self._create_control_panel(main_frame)
        
        # Start background updates
        self._start_background_updates()
    
    def _configure_styles(self):
        """Configure ttk styles for dark theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        accent_color = '#007acc'
        
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background=accent_color, foreground=fg_color)
        style.configure('TEntry', fieldbackground='#3c3c3c', foreground=fg_color)
        style.configure('TScrollbar', background=accent_color)
        
        # Custom styles
        style.configure('Chat.TFrame', background='#1e1e1e')
        style.configure('Peer.TFrame', background='#3c3c3c')
    
    def _create_chat_area(self, parent):
        """Create chat display and input area"""
        # Chat frame
        chat_frame = ttk.Frame(parent, style='Chat.TFrame')
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=60,
            height=25,
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='white',
            font=('Consolas', 10)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_display.config(state=tk.DISABLED)
        
        # Input frame
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X)
        
        # Message entry
        self.message_entry = ttk.Entry(
            input_frame,
            font=('Consolas', 10)
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind('<Return>', lambda e: self._send_message())
        
        # Send button
        send_btn = ttk.Button(
            input_frame,
            text="Send",
            command=self._send_message
        )
        send_btn.pack(side=tk.RIGHT)
    
    def _create_control_panel(self, parent):
        """Create peer list and control panel"""
        control_frame = ttk.Frame(parent, width=250)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        control_frame.pack_propagate(False)
        
        # Node info
        info_frame = ttk.Frame(control_frame, style='Peer.TFrame')
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            info_frame, 
            text=f"Node: {self.node.host}:{self.node.port}",
            font=('Consolas', 10, 'bold')
        ).pack(pady=5)
        
        # Connection frame
        conn_frame = ttk.LabelFrame(control_frame, text="Connect to Peer")
        conn_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Host entry
        ttk.Label(conn_frame, text="Host:").pack(anchor=tk.W)
        self.host_entry = ttk.Entry(conn_frame)
        self.host_entry.insert(0, "localhost")
        self.host_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Port entry
        ttk.Label(conn_frame, text="Port:").pack(anchor=tk.W)
        self.port_entry = ttk.Entry(conn_frame)
        self.port_entry.insert(0, "5000")
        self.port_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Connect button
        connect_btn = ttk.Button(
            conn_frame,
            text="Connect",
            command=self._connect_to_peer
        )
        connect_btn.pack(fill=tk.X)
        
        # Peers list
        peers_frame = ttk.LabelFrame(control_frame, text="Connected Peers")
        peers_frame.pack(fill=tk.BOTH, expand=True)
        
        # Peer listbox
        self.peers_listbox = tk.Listbox(
            peers_frame,
            bg='#3c3c3c',
            fg='#ffffff',
            selectbackground='#007acc',
            font=('Consolas', 9)
        )
        self.peers_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Peer controls frame
        peer_controls = ttk.Frame(peers_frame)
        peer_controls.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            peer_controls,
            text="Refresh",
            command=self._refresh_peers
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(
            peer_controls,
            text="Disconnect",
            command=self._disconnect_peer
        ).pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Security info
        security_frame = ttk.LabelFrame(control_frame, text="Security")
        security_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(
            security_frame,
            text="✓ End-to-End Encryption",
            foreground='#00ff00'
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Label(
            security_frame,
            text="✓ RSA Key Exchange",
            foreground='#00ff00'
        ).pack(anchor=tk.W, pady=2)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            control_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def _start_background_updates(self):
        """Start background thread for UI updates"""
        def update_loop():
            while self.root and self.node.running:
                try:
                    self._refresh_peers()
                    time.sleep(2)
                except Exception as e:
                    self.logger.error(f"Background update error: {e}")
                    time.sleep(5)
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
    
    def _update_chat_display(self, message: str):
        """Update chat display with new message"""
        if self.root:
            self.root.after(0, self._safe_chat_update, message)
    
    def _safe_chat_update(self, message: str):
        """Thread-safe chat display update"""
        try:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, message + '\n')
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
        except Exception as e:
            self.logger.error(f"Chat update error: {e}")
    
    def _update_peer_list(self):
        """Update the peer list display"""
        if self.root:
            self.root.after(0, self._safe_peer_update)
    
    def _safe_peer_update(self):
        """Thread-safe peer list update"""
        try:
            self.peers_listbox.delete(0, tk.END)
            peers = self.node.connection_manager.get_connected_peers()
            for peer_id in peers.keys():
                self.peers_listbox.insert(tk.END, peer_id)
        except Exception as e:
            self.logger.error(f"Peer update error: {e}")
    
    def _send_message(self):
        """Send message from input field"""
        message_text = self.message_entry.get().strip()
        if not message_text:
            return
        
        try:
            # Create and send message
            message = self.node.message_handler.create_chat_message(message_text)
            self.node.send_message(message)
            
            # Display own message
            timestamp = time.strftime("%H:%M:%S")
            self._update_chat_display(f"[{timestamp}] You: {message_text}")
            
            # Clear input
            self.message_entry.delete(0, tk.END)
            
        except Exception as e:
            self._show_error(f"Failed to send message: {e}")
    
    def _connect_to_peer(self):
        """Connect to peer using entered host/port"""
        host = self.host_entry.get().strip()
        port_str = self.port_entry.get().strip()
        
        if not host or not port_str:
            self._show_error("Please enter both host and port")
            return
        
        try:
            port = int(port_str)
            self.status_var.set(f"Connecting to {host}:{port}...")
            
            # Run connection in thread to avoid blocking GUI
            def connect_thread():
                try:
                    success = self.node.connect_to_peer(host, port)
                    if success:
                        self.root.after(0, lambda: self.status_var.set(f"Connected to {host}:{port}"))
                    else:
                        self.root.after(0, lambda: self.status_var.set(f"Failed to connect to {host}:{port}"))
                except Exception as e:
                    self.root.after(0, lambda: self._show_error(f"Connection failed: {e}"))
            
            threading.Thread(target=connect_thread, daemon=True).start()
            
        except ValueError:
            self._show_error("Port must be a valid number")
        except Exception as e:
            self._show_error(f"Connection error: {e}")
    
    def _refresh_peers(self):
        """Refresh peer list"""
        try:
            self._update_peer_list()
            self.status_var.set("Peers refreshed")
        except Exception as e:
            self.logger.error(f"Refresh peers error: {e}")
    
    def _disconnect_peer(self):
        """Disconnect selected peer"""
        try:
            selection = self.peers_listbox.curselection()
            if selection:
                peer_id = self.peers_listbox.get(selection[0])
                self.node.connection_manager._remove_connection(peer_id)
                self.status_var.set(f"Disconnected from {peer_id}")
                self._refresh_peers()
            else:
                self._show_error("Please select a peer to disconnect")
        except Exception as e:
            self._show_error(f"Disconnection error: {e}")
    
    def _show_error(self, message: str):
        """Show error message dialog"""
        if self.root:
            self.root.after(0, lambda: messagebox.showerror("Error", message))
    
    def _show_info(self, message: str):
        """Show info message dialog"""
        if self.root:
            self.root.after(0, lambda: messagebox.showinfo("Information", message))
