🏗️ Project Architecture
p2p-chat-app/
├── src/
│   ├── core/           # P2P networking logic
│   │   ├── p2p_node.py
│   │   ├── message_handler.py
│   │   └── connection_manager.py
│   ├── security/       # Encryption implementation
│   │   └── encryption.py
│   ├── network/        # Socket communication
│   │   └── protocol.py
│   ├── ui/            # User interfaces
│   │   ├── cli_interface.py
│   │   └── tkinter_gui.py
│   └── utils/         # Utility functions
│       └── logger.py
├── scripts/           # Automation scripts
├── config/           # Configuration files
└── docs/            # Documentation
