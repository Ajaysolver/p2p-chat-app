#!/usr/bin/env python3
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("🔍 Checking ALL imports...")

modules_to_check = [
    ('src.main', 'main'),
    ('src.core.p2p_node', 'P2PNode'),
    ('src.core.message_handler', 'MessageHandler'),
    ('src.core.connection_manager', 'ConnectionManager'),
    ('src.core.peer_discovery', 'PeerDiscovery'),
    ('src.security.encryption', 'EncryptionManager'),
    ('src.network.protocol', 'MessageProtocol'),
    ('src.ui.cli_interface', 'CLIInterface'),
    ('src.ui.gui_interface', 'GUIInterface'),
    ('src.utils.logger', 'get_logger'),
    ('src.utils.config_loader', 'ConfigLoader'),
]

all_good = True
for module_path, class_name in modules_to_check:
    try:
        module = __import__(module_path, fromlist=[class_name])
        obj = getattr(module, class_name) if class_name != 'main' else module.main
        print(f"✅ {module_path}.{class_name}")
    except ImportError as e:
        print(f"❌ {module_path}.{class_name} - {e}")
        all_good = False
    except AttributeError as e:
        print(f"❌ {module_path}.{class_name} - {e}")
        all_good = False

if all_good:
    print("\n🎉 ALL IMPORTS SUCCESSFUL!")
    print("You can now run: python run.py --port 5000 --gui")
else:
    print("\n💥 Some imports failed. Please check the errors above.")
