"""
Windows File Organizer - Automatic File Organization System
Author: Your Name
License: MIT
Description: Automatically organizes files from Downloads and Desktop folders
            with 30-minute delay before moving to destination folders.
"""

import os
import shutil
import time
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib
import sys

__version__ = "1.0.0"

class FileOrganizerHandler(FileSystemEventHandler):
    """
    Handles file system events and organizes files with delay.
    """
    def __init__(self, source_folder, dest_base, folder_name):
        self.source_folder = source_folder
        self.dest_base = dest_base
        self.folder_name = folder_name
        self.pending_files = {}  # Track files waiting to be moved
        self.delay_minutes = 30  # Wait 30 minutes before moving
        
        # File type mappings
        self.file_types = {
            'docx': ['.docx', '.doc'],
            'xlsx': ['.xlsx', '.xls'],
            'pdf': ['.pdf'],
            'jpg': ['.jpg', '.jpeg'],
            'png': ['.png'],
            'txt': ['.txt'],
            'pptx': ['.pptx', '.ppt'],
            'zip': ['.zip', '.rar', '.7z'],
            'mp4': ['.mp4', '.avi', '.mkv', '.mov'],
            'mp3': ['.mp3', '.wav', '.flac']
        }
    
    def get_file_hash(self, filepath):
        """Calculate MD5 hash of file for duplicate detection"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"Error calculating hash: {e}")
            return None
    
    def get_destination_path(self, file_path):
        """Generate destination path based on year/month/filetype structure"""
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m_%B")  # 01_January format
        
        file_ext = Path(file_path).suffix.lower()
        
        # Determine file type folder
        type_folder = "others"
        for folder, extensions in self.file_types.items():
            if file_ext in extensions:
                type_folder = folder
                break
        
        # Build destination path: F:\IN_MSG\2025\01_January\docx\
        dest_path = os.path.join(
            self.dest_base,
            self.folder_name,
            year,
            month,
            type_folder
        )
        
        return dest_path
    
    def handle_duplicate(self, source_file, dest_file):
        """Handle duplicate files - compare and decide action"""
        source_hash = self.get_file_hash(source_file)
        dest_hash = self.get_file_hash(dest_file)
        
        source_mtime = os.path.getmtime(source_file)
        dest_mtime = os.path.getmtime(dest_file)
        
        # If files are identical (same hash), skip
        if source_hash == dest_hash:
            print(f"✓ Identical file exists, skipping: {os.path.basename(source_file)}")
            os.remove(source_file)
            return
        
        # If source is newer, replace
        if source_mtime > dest_mtime:
            print(f"↻ Replacing with newer version: {os.path.basename(source_file)}")
            os.remove(dest_file)
            shutil.move(source_file, dest_file)
            return
        
        # Otherwise, create versioned file
        base_name = Path(dest_file).stem
        extension = Path(dest_file).suffix
        dest_dir = Path(dest_file).parent
        
        version = 1
        while True:
            new_name = f"{base_name}_v{version}{extension}"
            new_path = dest_dir / new_name
            if not new_path.exists():
                print(f"✓ Creating versioned file: {new_name}")
                shutil.move(source_file, str(new_path))
                break
            version += 1
    
    def organize_file(self, file_path):
        """Move and organize a single file"""
        if not os.path.isfile(file_path):
            return
        
        # Skip temporary and system files
        filename = os.path.basename(file_path)
        if filename.startswith('.') or filename.startswith('~') or filename.startswith('$'):
            return
        
        try:
            dest_folder = self.get_destination_path(file_path)
            
            # Create destination folder if it doesn't exist
            os.makedirs(dest_folder, exist_ok=True)
            
            dest_file = os.path.join(dest_folder, filename)
            
            # Handle duplicates
            if os.path.exists(dest_file):
                self.handle_duplicate(file_path, dest_file)
            else:
                shutil.move(file_path, dest_file)
                print(f"✓ Moved: {filename}")
                print(f"  → {dest_folder}")
        
        except Exception as e:
            print(f"✗ Error organizing {filename}: {str(e)}")
    
    def on_created(self, event):
        """Handle new file creation - add to pending queue"""
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            if not filename.startswith('.') and not filename.startswith('~') and not filename.startswith('$'):
                # Record the time when file was created
                self.pending_files[event.src_path] = time.time()
                print(f"\n⏱️  New file detected: {filename}")
                print(f"   Will move in {self.delay_minutes} minutes")
    
    def on_modified(self, event):
        """Handle file modification - update the timer"""
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            if not filename.startswith('.') and not filename.startswith('~') and not filename.startswith('$'):
                # Update the time - restart the 30 minute timer
                if event.src_path in self.pending_files:
                    self.pending_files[event.src_path] = time.time()
                    print(f"\n↻ File modified: {filename}")
                    print(f"   Timer reset - will move in {self.delay_minutes} minutes")
    
    def check_pending_files(self):
        """Check if any pending files are ready to be moved"""
        current_time = time.time()
        delay_seconds = self.delay_minutes * 60
        
        files_to_move = []
        for file_path, added_time in list(self.pending_files.items()):
            if current_time - added_time >= delay_seconds:
                files_to_move.append(file_path)
        
        for file_path in files_to_move:
            if os.path.exists(file_path):
                print(f"\n⏰ 30 minutes elapsed!")
                self.organize_file(file_path)
            del self.pending_files[file_path]

def organize_existing_files(source_folder, dest_base, folder_name):
    """Organize all existing files in the source folder (optional function)"""
    handler = FileOrganizerHandler(source_folder, dest_base, folder_name)
    
    print(f"\nOrganizing existing files in {source_folder}...")
    file_count = 0
    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)
        if os.path.isfile(file_path):
            handler.organize_file(file_path)
            file_count += 1
    print(f"✓ {file_count} existing files organized!\n")

def main():
    """Main function to start the file organizer"""
    print(f"\n{'=' * 70}")
    print(f"  WINDOWS FILE ORGANIZER v{__version__}")
    print(f"  Automatic File Organization with 30-Minute Delay")
    print(f"{'=' * 70}\n")
    
    # Get user folders
    downloads_folder = str(Path.home() / "Downloads")
    desktop_folder = str(Path.home() / "Desktop")
    
    # Destination drives (modify these as needed)
    f_drive = "F:\\"
    d_drive = "D:\\"
    
    # Check if drives exist
    drives_ok = True
    if not os.path.exists(f_drive):
        print(f"⚠️  Warning: F: drive not found!")
        drives_ok = False
    if not os.path.exists(d_drive):
        print(f"⚠️  Warning: D: drive not found!")
        drives_ok = False
    
    if not drives_ok:
        print("\n❌ Please check your drive configuration and try again.")
        print("   Edit the script to change drive letters if needed.\n")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print("📁 Monitoring Folders:")
    print(f"   Downloads → F:\\IN_MSG\\YYYY\\MM_Month\\filetype\\")
    print(f"   Desktop   → D:\\OUT_MSG\\YYYY\\MM_Month\\filetype\\")
    print(f"\n⏱️  Delay: Files will move 30 minutes after creation/last modification")
    print(f"\n💡 Tip: Press Ctrl+C to stop the organizer")
    print(f"{'=' * 70}\n")
    
    # Note about existing files
    print("ℹ️  Note: Only NEW files will be organized automatically.")
    print("   Existing files in folders will not be touched.\n")
    
    observers = []
    handlers = []
    
    # Setup Downloads folder monitoring
    if os.path.exists(downloads_folder):
        downloads_handler = FileOrganizerHandler(downloads_folder, f_drive, "IN_MSG")
        downloads_observer = Observer()
        downloads_observer.schedule(downloads_handler, downloads_folder, recursive=False)
        downloads_observer.start()
        observers.append(downloads_observer)
        handlers.append(downloads_handler)
        print(f"✓ Monitoring: {downloads_folder}")
    
    # Setup Desktop folder monitoring
    if os.path.exists(desktop_folder):
        desktop_handler = FileOrganizerHandler(desktop_folder, d_drive, "OUT_MSG")
        desktop_observer = Observer()
        desktop_observer.schedule(desktop_handler, desktop_folder, recursive=False)
        desktop_observer.start()
        observers.append(desktop_observer)
        handlers.append(desktop_handler)
        print(f"✓ Monitoring: {desktop_folder}")
    
    print(f"\n{'=' * 70}")
    print("🟢 File Organizer is now running...")
    print(f"{'=' * 70}\n")
    
    try:
        while True:
            time.sleep(10)  # Check every 10 seconds
            for handler in handlers:
                handler.check_pending_files()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("🛑 Stopping File Organizer...")
        print("=" * 70)
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()
        print("\n✓ File Organizer stopped successfully!")
        print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
