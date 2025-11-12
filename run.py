'ENDOFFILE'
#!/usr/bin/env python3
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Now import from src
from src.main import main

if __name__ == "__main__":
    main()
ENDOFFILE
