import subprocess
import sys
from pathlib import Path
import importlib.util

# Move configuration to the top
PACKAGE_MAP = {
    "psycopg2-binary": "psycopg2",
    "python-dotenv": "dotenv",
    "pyyaml": "yaml"
}

def install_requirements(file_path: str = 'requirements.txt') -> None:
    """
    Checks for missing Python packages and installs them via pip.
    Resolves naming discrepancies between pip install names and import names.
    """
    req_file = Path(file_path)
    
    if not req_file.exists():
        print(f"❌ Error: {file_path} not found.")
        return

    # 1. Parse packages from requirements.txt
    with open(req_file, 'r') as f:
        packages = [
            line.split('==')[0].strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

    # 2. Identify missing packages
    missing_packages = []
    for package in packages:
        # Resolve import name using map or default normalization
        import_name = PACKAGE_MAP.get(package.lower(), package.replace('-', '_'))
        
        if importlib.util.find_spec(import_name) is None:
            missing_packages.append(package)

    # 3. Execution logic
    if not missing_packages:
        print("✅ All requirements already satisfied.")
        return

    print(f"📦 Installing missing packages: {', '.join(missing_packages)}...")

    try:
        # Use sys.executable to ensure we use the current virtual environment
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *missing_packages],
            stdout=subprocess.DEVNULL  # Keeps your console clean
        )
        print("🚀 Done! Environment is ready.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed with error: {e}")
