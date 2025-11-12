### Starting the Application
1. Run `./scripts/start_gui.sh` for graphical interface
2. Or `python run.py --port 5000` for command line

### Connecting to Peers
1. Get the IP address and port of another user
2. In the application, use: `connect <IP> <port>`
3. Example: `connect 192.168.1.5 5001`

### Sending Messages
- Type your message and press Enter
- Messages are encrypted automatically
- See delivery status in the interface

## Features Explained

### Security Indicators
- 🔒 Lock icon: Message encrypted
- ✅ Checkmark: Message delivered
- ⏳ Clock: Message sending

### Connection Management
- View connected peers in the side panel
- Monitor connection quality
- Manage multiple simultaneous chats
