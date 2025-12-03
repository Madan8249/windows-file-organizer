# Windows File Organizer v5.0.0 - Advanced Edition 🚀

Intelligent file organization system with advanced features, JSON configuration, and comprehensive statistics tracking.

![Version](https://img.shields.io/badge/version-5.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey)

## 🆕 What's New in v5.0.0

### Advanced Features
- ✅ **JSON Configuration** - Easy configuration without editing code
- ✅ **Configurable Delay** - Set any delay time (not just 30 minutes)
- ✅ **Multiple Sources** - Monitor unlimited folders
- ✅ **Statistics Tracking** - Detailed stats with file type breakdown
- ✅ **File Logging** - Log to file + console
- ✅ **10 File Categories** - Extended file type support
- ✅ **Smart Exclusions** - Skip temp files, system files
- ✅ **Better Error Handling** - Comprehensive error management
- ✅ **Session History** - Track usage over time

### Comparison with v1.0.0

| Feature | v1.0.0 | v5.0.0 |
|---------|--------|--------|
| Configuration | Hardcoded | JSON File ✨ |
| Delay Time | Fixed 30 min | Configurable ✨ |
| Source Folders | 2 Fixed | Unlimited ✨ |
| File Categories | 8 types | 10+ types ✨ |
| Statistics | None | Full tracking ✨ |
| Logging | Console | File + Console ✨ |
| Exclusions | Basic | Advanced ✨ |
| Error Handling | Basic | Comprehensive ✨ |

## 📋 Features

### Core Features
- ⏱️ **Configurable Delay**: Set custom wait time before organizing
- 📁 **Smart Organization**: Year/Month/FileType structure
- 🔄 **Duplicate Handling**: Replace newer, version older files
- 🚀 **Auto-Start**: Run automatically at Windows startup
- 📊 **Statistics**: Track all file operations
- 📝 **Logging**: Console and file logging
- ⚙️ **Easy Configuration**: JSON-based settings

### File Categories
Documents, Spreadsheets, Presentations, Images, Videos, Audio, Archives, Code, Executables, Ebooks, and Others

## 🔧 Requirements

- Windows 10 or 11
- Python 3.7+
- Required drives (configurable in config.json)

## 📥 Installation

### Quick Install
```bash
# 1. Clone repository
https://github.com/soren-code/windows-file-organizer.git
cd windows-file-organizer/v5.0.0

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure
# Edit config.json for your settings

# 4. Run
python file_organizer_v5.py
```

### Detailed Installation

See [INSTALLATION_GUIDE_v5.md](INSTALLATION_GUIDE_v5.md)

## ⚙️ Configuration

Edit `config.json` to customize:

### Change Delay Time
```json
"general": {
    "delay_minutes": 15  // Change to any number
}
```

### Change Drives
```json
"sources": [
    {
        "name": "Downloads",
        "destination_drive": "E:\\",  // Your drive
        "destination_folder": "MyFiles"
    }
]
```

### Add More Sources
```json
"sources": [
    {
        "name": "Documents",
        "folder": "Documents",
        "destination_drive": "G:\\",
        "destination_folder": "DOCS",
        "enabled": true
    }
]
```

### Add Custom File Types
```json
"file_types": {
    "3d_models": [".obj", ".stl", ".fbx"],
    "databases": [".db", ".sql", ".mdb"]
}
```

### Exclude Specific Files
```json
"exclusions": {
    "exclude_files": ["myfile.txt", "important.docx"]
}
```

## 🚀
