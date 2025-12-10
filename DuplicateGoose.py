"""
DuplicateGoose.py
--------------------
Is added to Start-up folder to duplicate the shortcut upon start-up. 
"""

import shutil
import os
from pathlib import Path
from datetime import datetime

def get_base_path():
    """Return folder where EXE/script is located."""
    if getattr(sys, "frozen", False):
        # Running as EXE
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent

def duplicate_exe():
    """Duplicate any file named GooseDesktop (with any extension)."""
    try:
        # Get the directory where this script is located
        script_dir = get_base_path()
        
        # Find any file named GooseDesktop with any extension
        goose_file = None
        for file in script_dir.iterdir():
            if file.is_file() and file.stem == "GooseDesktop":
                goose_file = file
                break
        
        if goose_file is None:
            print(f"✗ No file named GooseDesktop found in {script_dir}")
            return False
        
        # Create a duplicate with a timestamp to make it unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        duplicate_path = script_dir / f"GooseDesktop_{timestamp}{goose_file.suffix}"
        
        # Copy the file
        shutil.copy2(goose_file, duplicate_path)
        print(f"✓ Duplicated: {goose_file.name} → {duplicate_path.name}")
        return True
    
    except Exception as e:
        print(f"✗ Error duplicating file: {e}")
        return False

if __name__ == "__main__":
    duplicate_exe()
