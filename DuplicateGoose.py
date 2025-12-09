"""
Is added to Start-up folder to duplicate the shortcut upon start-up. 
"""

import shutil
import os
from pathlib import Path
from datetime import datetime

def duplicate_exe():
    """Duplicate GooseDesktop.exe in the current folder."""
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        
        # Find GooseDesktop.exe
        exe_path = script_dir / "GooseDesktop.exe"
        
        if not exe_path.exists():
            print(f"✗ GooseDesktop.exe not found in {script_dir}")
            return False
        
        # Create a duplicate with a timestamp to make it unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        duplicate_path = script_dir / f"GooseDesktop_{timestamp}.exe"
        
        # Copy the file
        shutil.copy2(exe_path, duplicate_path)
        print(f"✓ Duplicated: {exe_path.name} → {duplicate_path.name}")
        return True
    
    except Exception as e:
        print(f"✗ Error duplicating file: {e}")
        return False

if __name__ == "__main__":
    duplicate_exe()