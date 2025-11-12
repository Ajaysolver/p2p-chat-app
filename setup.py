'EOF'
from setuptools import setup, find_packages

setup(
    name="p2p-chat-app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "cryptography>=3.4.8",
        "pycryptodome>=3.10.1",
        "requests>=2.25.1",
    ],
    entry_points={
        'console_scripts': [
            'p2p-chat=run:main',
        ],
    },
    python_requires='>=3.7',
)
EOF
