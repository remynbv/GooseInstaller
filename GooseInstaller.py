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

def get_base_path():
    """Return folder where EXE/script is located."""
    if getattr(sys, "frozen", False):
        # Running as EXE
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent

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

def copy_file_to_startup(source_file, destination_name=None):
    """Copy a file to the startup folder."""
    try:
        source_path = Path(source_file)
        
        if not source_path.exists():
            print(f"✗ File not found: {source_path}")
            return False
        
        # Get startup folder path
        startup_folder = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        
        if not startup_folder.exists():
            print(f"✗ Startup folder not found: {startup_folder}")
            return False
        
        if destination_name is None:
            destination_name = source_path.name
        
        destination_file = startup_folder / destination_name
        
        # Copy the file
        shutil.copy2(source_path, destination_file)
        print(f"✓ File copied to startup: {destination_file}")
        return True
    except Exception as e:
        print(f"✗ Failed to copy file to startup: {e}")
        return False

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

def main():
    """Main installation function."""
    print("=" * 50)
    print("Desktop Goose Auto-installer")
    print("=" * 50)
    
    # Get the directory where the script is located
    script_dir = get_base_path()
    
    # Look specifically for 'Desktop Goose' folder
    source_folder = script_dir / "Desktop Goose"
    
    if not source_folder.exists() or not source_folder.is_dir():
        print(f"✗ 'Desktop Goose' folder not found in {script_dir}")
        return False
    
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
    
    # Step 3: Create startup shortcut for GooseDesktop.exe
    print("\n[3/4] Creating startup shortcut for GooseDesktop.exe...")
    goose_exe = destination_folder / "GooseDesktop.exe"
    
    if not goose_exe.exists():
        print(f"✗ GooseDesktop.exe not found in {destination_folder}")
        return False
    
    if not create_startup_shortcut(str(goose_exe)):
        return False
    
    # Step 4: Copy DuplicateGoose.exe from dist to startup folder
    print("\n[4/4] Copying DuplicateGoose.exe to startup...")
    #duplicate_exe = script_dir / "dist" / "DuplicateGoose" / "DuplicateGoose.exe"
    duplicate_exe = script_dir / "DuplicateGoose.exe"
    
    if not duplicate_exe.exists():
        print(f"⚠ Warning: DuplicateGoose.exe not found at {duplicate_exe}, but installation otherwise complete")
    else:
        if not copy_file_to_startup(str(duplicate_exe)):
            print("⚠ Warning: Could not copy DuplicateGoose.exe, but installation otherwise complete")
    
    print("\n" + "=" * 50)
    print("✓ Installation completed successfully!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
