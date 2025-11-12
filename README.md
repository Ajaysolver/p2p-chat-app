# P2P Secure Chat Application

A Linux-based peer-to-peer chat application with end-to-end encryption, built for Kali Linux.

## Features
- Peer-to-peer architecture
- End-to-end encryption
- No central server required
- Cross-platform compatibility
- Secure key exchange

## Quick Start on Kali Linux

```bash
# Install dependencies
./scripts/install_dependencies.sh

# Activate virtual environment
source p2p-env/bin/activate

# Run first instance
python run.py --port 5000

# In another terminal, run second instance
python run.py --port 5001

# Connect them
/connect localhost 5000  # from the second instance
