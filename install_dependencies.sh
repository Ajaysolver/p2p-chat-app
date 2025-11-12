'EOF'
#!/bin/bash

echo "Installing P2P Chat Dependencies on Kali Linux..."

# Update system
sudo apt update

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv python3-tk

# Install system dependencies for cryptography
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

# Create virtual environment
python3 -m venv p2p-env
source p2p-env/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Install additional GUI dependencies
pip install pillow  # For enhanced GUI capabilities

# Make scripts executable
chmod +x scripts/*.sh
chmod +x run.py

echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo "To activate virtual environment:"
echo "  source p2p-env/bin/activate"
echo ""
echo "To run with GUI:"
echo "  python run.py --port 5000 --gui"
echo ""
echo "To run in CLI mode:"
echo "  python run.py --port 5000"
echo ""
echo "Connect multiple instances:"
echo "  Terminal 1: python run.py --port 5000 --gui"
echo "  Terminal 2: python run.py --port 5001 --gui"
echo "  Then connect via GUI from port 5001 to localhost:5000"
echo "=========================================="
EOF

chmod +x scripts/install_dependencies.sh
