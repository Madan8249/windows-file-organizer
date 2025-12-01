"""
Windows File Organizer v5.0.0 - Advanced Edition
Author: Your Name
License: MIT

New Features in v5.0.0:
- JSON configuration file
- Configurable delay time
- Multiple source folders support
- Advanced statistics tracking
- File logging support
- Custom file type rules
- Exclude patterns
- Better error handling
- Progress tracking
"""

import os
import shutil
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib
import sys

__version__ = "5.0.0"

# Configuration Manager
class ConfigManager:
    """Manage configuration from JSON file"""
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.settings = self.load_or_create_config()
    
    def load_or_create_config(self):
        """Load existing config or create default"""
        default_config = {
            "version": "5.0.0",
            "general": {
                "delay_minutes": 30,
                "organize_existing_on_startup": False,
                "check_interval_seconds": 10
            },
            "logging": {
                "log_to_file": True,
                "log_file": "file_organizer.log",
                "log_level": "INFO",
                "console_output": True
            },
            "sources": [
                {
                    "name": "Downloads",
                    "folder": "Downloads",
                    "destination_drive": "F:\\",
                    "destination_folder": "IN_MSG",
                    "enabled": True
                },
                {
                    "name": "Desktop",
                    "folder": "Desktop",
                    "destination_drive": "D:\\",
                    "destination_folder": "OUT_MSG",
                    "enabled": True
                }
            ],
            "file_types": {
                "documents": [".docx", ".doc", ".txt", ".pdf", ".odt", ".rtf"],
                "spreadsheets": [".xlsx", ".xls", ".csv", ".ods"],
                "presentations": [".pptx", ".ppt", ".odp"],
                "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico"],
                "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
                "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
                "archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
                "code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".json", ".xml"],
                "executables": [".exe", ".msi", ".bat", ".sh", ".app"],
                "ebooks": [".epub", ".mobi", ".azw", ".azw3"]
            },
            "exclusions": {
                "exclude_prefixes": [".", "~", "$"],
                "exclude_files": ["desktop.ini", "Thumbs.db", ".DS_Store"],
                "exclude_extensions": [".tmp", ".temp", ".crdownload", ".part"]
            },
            "statistics": {
                "enabled": True,
                "stats_file": "statistics.json",
                "show_on_exit": True
            },
            "notifications": {
                "enabled": False,
                "show_move_notification": True,
                "show_error_notification": True
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Deep merge
                    self._deep_merge(default_config, loaded)
                    return default_config
            except Exception as e:
                print(f"⚠️  Error loading config: {e}")
                print("   Using default configuration.")
                self.save_config(default_config)
                return default_config
        else:
            print(f"📝 Creating default config file: {self.config_file}")
            self.save_config(default_config)
            return default_config
    
    def _deep_merge(self, base, update):
        """Recursively merge dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def save_config(self, config=None):
        """Save configuration to file"""
        if config is None:
            config = self.settings
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving config: {e}")

# Statistics Tracker
class StatisticsTracker:
    """Track and manage file organization statistics"""
    def __init__(self, stats_file="statistics.json", enabled=True):
        self.stats_file = stats_file
        self.enabled = enabled
        self.stats = self.load_stats()
    
    def load_stats(self):
        """Load statistics from file"""
        default_stats = {
            "session_start": datetime.now().isoformat(),
            "last_updated": None,
            "totals": {
                "files_moved": 0,
                "files_skipped": 0,
                "files_versioned": 0,
                "files_replaced": 0,
                "errors": 0
            },
            "by_type": {},
            "by_date": {},
            "sessions": []
        }
        
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Keep history, just update session_start
                    loaded["session_start"] = datetime.now().isoformat()
                    return loaded
            except:
                return default_stats
        return default_stats
    
    def save_stats(self):
        """Save statistics to file"""
        if not self.enabled:
            return
        
        try:
            self.stats["last_updated"] = datetime.now().isoformat()
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving statistics: {e}")
    
    def increment(self, action, file_type=None):
        """Increment a statistic"""
        if not self.enabled:
            return
        
        # Update totals
        if action in self.stats["totals"]:
            self.stats["totals"][action] += 1
        
        # Update by file type
        if file_type:
            if file_type not in self.stats["by_type"]:
                self.stats["by_type"][file_type] = 0
            self.stats["by_type"][file_type] += 1
        
        # Update by date
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.stats["by_date"]:
            self.stats["by_date"][today] = {"files_moved": 0, "errors": 0}
        
        if action == "files_moved":
            self.stats["by_date"][today]["files_moved"] += 1
        elif action == "errors":
            self.stats["by_date"][today]["errors"] += 1
        
        self.save_stats()
    
    def get_summary(self):
        """Get statistics summary"""
        return self.stats["totals"]
    
    def print_statistics(self):
        """Print formatted statistics"""
        print("\n" + "=" * 80)
        print("📊 FILE ORGANIZER STATISTICS")
        print("=" * 80)
        
        totals = self.stats["totals"]
        print(f"\n📈 Session Totals:")
        print(f"   Files Moved:     {totals['files_moved']:,}")
        print(f"   Files Skipped:   {totals['files_skipped']:,}")
        print(f"   Files Versioned: {totals['files_versioned']:,}")
        print(f"   Files Replaced:  {totals['files_replaced']:,}")
        print(f"   Errors:          {totals['errors']:,}")
        
        if self.stats["by_type"]:
            print(f"\n📁 By File Type:")
            sorted_types = sorted(self.stats["by_type"].items(), key=lambda x: x[1], reverse=True)
            for file_type, count in sorted_types[:10]:  # Top 10
                print(f"   {file_type:15} {count:,}")
        
        if self.stats["by_date"]:
            print(f"\n📅 Recent Activity:")
            recent_dates = sorted(self.stats["by_date"].items(), reverse=True)[:7]  # Last 7 days
            for date, data in recent_dates:
                print(f"   {date}: {data['files_moved']:,} files moved")
        
        print("\n" + "=" * 80 + "\n")

# Advanced File Organizer Handler
class AdvancedFileOrganizerHandler(FileSystemEventHandler):
    """Advanced file organization with v5.0.0 features"""
    
    def __init__(self, source_config, config_manager, statistics):
        self.source_config = source_config
        self.config = config_manager
        self.stats = statistics
        
        # Source and destination
        self.source_folder = str(Path.home() / source_config["folder"])
        self.dest_base = source_config["destination_drive"]
        self.dest_folder = source_config["destination_folder"]
        self.name = source_config["name"]
        
        # Settings
        self.delay_minutes = config_manager.settings["general"]["delay_minutes"]
        self.file_types = config_manager.settings["file_types"]
        self.exclusions = config_manager.settings["exclusions"]
        
        # Pending files queue
        self.pending_files = {}
        
        # Logger
        self.logger = logging.getLogger(__name__)
    
    def get_file_hash(self, filepath):
        """Calculate MD5 hash for duplicate detection"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Hash calculation error: {e}")
            return None
    
    def get_file_type_category(self, file_ext):
        """Get file type category"""
        for category, extensions in self.file_types.items():
            if file_ext in extensions:
                return category
        return "others"
    
    def get_destination_path(self, file_path):
        """Generate organized destination path"""
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m_%B")
        
        file_ext = Path(file_path).suffix.lower()
        type_category = self.get_file_type_category(file_ext)
        
        dest_path = os.path.join(
            self.dest_base,
            self.dest_folder,
            year,
            month,
            type_category
        )
        
        return dest_path, type_category
    
    def should_exclude(self, filename):
        """Check if file should be excluded"""
        # Check prefixes
        for prefix in self.exclusions["exclude_prefixes"]:
            if filename.startswith(prefix):
                return True
        
        # Check specific files
        if filename in self.exclusions["exclude_files"]:
            return True
        
        # Check extensions
        file_ext = Path(filename).suffix.lower()
        if file_ext in self.exclusions["exclude_extensions"]:
            return True
        
        return False
    
    def handle_duplicate(self, source_file, dest_file):
        """Smart duplicate handling"""
        source_hash = self.get_file_hash(source_file)
        dest_hash = self.get_file_hash(dest_file)
        
        filename = os.path.basename(source_file)
        
        # Identical files - skip
        if source_hash == dest_hash:
            self.logger.info(f"   ✓ Identical file exists, skipping: {filename}")
            os.remove(source_file)
            self.stats.increment("files_skipped")
            return
        
        # Compare modification times
        source_mtime = os.path.getmtime(source_file)
        dest_mtime = os.path.getmtime(dest_file)
        
        # Newer file - replace
        if source_mtime > dest_mtime:
            self.logger.info(f"   ↻ Replacing with newer version: {filename}")
            os.remove(dest_file)
            shutil.move(source_file, dest_file)
            self.stats.increment("files_replaced")
            return
        
        # Older file - create version
        base_name = Path(dest_file).stem
        extension = Path(dest_file).suffix
        dest_dir = Path(dest_file).parent
        
        version = 1
        while True:
            new_name = f"{base_name}_v{version}{extension}"
            new_path = dest_dir / new_name
            if not new_path.exists():
                self.logger.info(f"   ✓ Creating versioned file: {new_name}")
                shutil.move(source_file, str(new_path))
                self.stats.increment("files_versioned")
                break
            version += 1
    
    def organize_file(self, file_path):
        """Organize a single file"""
        if not os.path.isfile(file_path):
            return
        
        filename = os.path.basename(file_path)
        
        # Check exclusions
        if self.should_exclude(filename):
            self.logger.debug(f"Skipping excluded file: {filename}")
            return
        
        try:
            dest_path, file_category = self.get_destination_path(file_path)
            os.makedirs(dest_path, exist_ok=True)
            dest_file = os.path.join(dest_path, filename)
            
            self.logger.info(f"\n📦 Processing: {filename}")
            
            # Handle duplicates or move
            if os.path.exists(dest_file):
                self.handle_duplicate(file_path, dest_file)
            else:
                shutil.move(file_path, dest_file)
                self.logger.info(f"   ✓ Moved successfully")
                self.logger.info(f"   → {dest_path}")
                self.stats.increment("files_moved", file_category)
        
        except PermissionError as e:
            self.logger.error(f"   ✗ Permission denied: {filename}")
            self.stats.increment("errors")
        except Exception as e:
            self.logger.error(f"   ✗ Error organizing {filename}: {str(e)}")
            self.stats.increment("errors")
    
    def on_created(self, event):
        """Handle new file creation"""
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            
            if not self.should_exclude(filename):
                self.pending_files[event.src_path] = time.time()
                self.logger.info(f"\n⏱️  New file detected: {filename} ({self.name})")
                self.logger.info(f"   Will organize in {self.delay_minutes} minutes")
    
    def on_modified(self, event):
        """Handle file modification - reset timer"""
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            
            if not self.should_exclude(filename):
                if event.src_path in self.pending_files:
                    self.pending_files[event.src_path] = time.time()
                    self.logger.info(f"\n↻ File modified: {filename} ({self.name})")
                    self.logger.info(f"   Timer reset - {self.delay_minutes} minutes")
    
    def check_pending_files(self):
        """Check pending files and organize if delay elapsed"""
        current_time = time.time()
        delay_seconds = self.delay_minutes * 60
        
        files_to_move = []
        for file_path, added_time in list(self.pending_files.items()):
            if current_time - added_time >= delay_seconds:
                files_to_move.append(file_path)
        
        for file_path in files_to_move:
            if os.path.exists(file_path):
                self.logger.info(f"\n⏰ {self.delay_minutes} minutes elapsed!")
                self.organize_file(file_path)
            del self.pending_files[file_path]
    
    def organize_existing_files(self):
        """Organize all existing files in source folder"""
        if not os.path.exists(self.source_folder):
            return
        
        self.logger.info(f"\n📂 Organizing existing files in {self.name}...")
        count = 0
        
        for file in os.listdir(self.source_folder):
            file_path = os.path.join(self.source_folder, file)
            if os.path.isfile(file_path):
                self.organize_file(file_path)
                count += 1
        
        self.logger.info(f"   ✓ Organized {count} existing files from {self.name}\n")

def setup_logging(config):
    """Setup logging system"""
    log_config = config.settings["logging"]
    
    # Log level
    log_level = getattr(logging, log_config.get("log_level", "INFO"))
    
    # Format
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Handlers
    handlers = []
    
    if log_config.get("console_output", True):
        handlers.append(logging.StreamHandler(sys.stdout))
    
    if log_config.get("log_to_file", False):
        log_file = log_config.get("log_file", "file_organizer.log")
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )

def print_header():
    """Print application header"""
    print("\n" + "=" * 80)
    print("  🚀 WINDOWS FILE ORGANIZER v5.0.0 - ADVANCED EDITION")
    print("  Intelligent File Organization with Advanced Features")
    print("=" * 80 + "\n")

def print_config_info(config):
    """Print configuration information"""
    general = config.settings["general"]
    logging_config = config.settings["logging"]
    stats_config = config.settings["statistics"]
    
    print("⚙️  Configuration:")
    print(f"   Delay: {general['delay_minutes']} minutes")
    print(f"   Check Interval: {general['check_interval_seconds']} seconds")
    print(f"   Log to File: {logging_config['log_to_file']}")
    print(f"   Statistics: {stats_config['enabled']}")
    print()

def main():
    """Main application entry point"""
    
    # Print header
    print_header()
    
    # Load configuration
    print("📝 Loading configuration...")
    config = ConfigManager()
    print("   ✓ Configuration loaded\n")
    
    # Setup logging
    setup_logging(config)
    logger = logging.getLogger(__name__)
    
    # Initialize statistics
    stats_config = config.settings["statistics"]
    statistics = StatisticsTracker(
        stats_file=stats_config.get("stats_file", "statistics.json"),
        enabled=stats_config.get("enabled", True)
    )
    
    # Print configuration info
    print_config_info(config)
    
    # Setup file organizers
    observers = []
    handlers = []
    
    logger.info("🔍 Setting up file monitors...\n")
    
    for source_config in config.settings["sources"]:
        if not source_config.get("enabled", True):
            logger.info(f"⊘ Skipping disabled source: {source_config['name']}")
            continue
        
        source_folder = str(Path.home() / source_config["folder"])
        dest_drive = source_config["destination_drive"]
        
        # Check source exists
        if not os.path.exists(source_folder):
            logger.warning(f"⚠️  Source not found: {source_folder}")
            continue
        
        # Check destination drive exists
        if not os.path.exists(dest_drive):
            logger.warning(f"⚠️  Destination drive not found: {dest_drive}")
            continue
        
        # Create handler
        handler = AdvancedFileOrganizerHandler(source_config, config, statistics)
        
        # Organize existing files if configured
        if config.settings["general"].get("organize_existing_on_startup", False):
            handler.organize_existing_files()
        
        # Setup observer
        observer = Observer()
        observer.schedule(handler, source_folder, recursive=False)
        observer.start()
        
        observers.append(observer)
        handlers.append(handler)
        
        logger.info(f"✓ Monitoring: {source_config['name']}")
        logger.info(f"  Source: {source_folder}")
        logger.info(f"  Destination: {dest_drive}{source_config['destination_folder']}\n")
    
    if not observers:
        logger.error("❌ No valid sources to monitor!")
        logger.error("   Please check your config.json file.\n")
        return
    
    print("=" * 80)
    print("🟢 File Organizer is now running...")
    print("💡 Press Ctrl+C to stop and view statistics")
    print("=" * 80 + "\n")
    
    # Main loop
    try:
        check_interval = config.settings["general"].get("check_interval_seconds", 10)
        
        while True:
            time.sleep(check_interval)
            for handler in handlers:
                handler.check_pending_files()
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 80)
        print("🛑 Stopping File Organizer...")
        print("=" * 80 + "\n")
        
        # Stop observers
        for observer in observers:
            observer.stop()
        for observer in observers:
            observer.join()
        
        # Show statistics
        if config.settings["statistics"].get("show_on_exit", True):
            statistics.print_statistics()
        
        logger.info("✓ File Organizer stopped successfully!\n")

if __name__ == "__main__":
    main()
