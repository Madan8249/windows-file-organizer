# Changelog

All notable changes to this project will be documented in this file.

# Changelog

## [5.0.0] - 2025-02-01

### Added
- GUI configuration panel with system tray icon
- Cloud storage support (OneDrive, Google Drive, Dropbox)
- Real-time desktop notifications
- Custom rules engine for advanced filtering
- Multi-language support (English, Hindi, Spanish, French)
- Statistics dashboard
- Network drive support
- Email notifications
- Scheduled organization (work hours only)
- Exclude folders feature

### Changed
- Improved duplicate detection with fuzzy matching
- Faster file monitoring (50% performance improvement)
- Better error handling and logging
- Updated UI/UX for configuration

### Fixed
- Memory leak in long-running sessions
- Unicode filename handling
- Large file (>5GB) moving issues

---


## [1.0.0] - 2025-01-30

### Added
- Initial release
- Automatic file organization from Downloads and Desktop folders
- 30-minute delay before moving files
- Smart duplicate handling (replace/version/skip)
- Support for multiple file types (docx, xlsx, pdf, jpg, png, etc.)
- Automatic folder creation by Year/Month/FileType
- Timer reset on file modification
- Background operation support
- Auto-start with Windows capability
- Comprehensive logging and status messages
- Hash-based duplicate detection
- Version control for older duplicate files

### Features
- Monitors Downloads → F:\IN_MSG
- Monitors Desktop → D:\OUT_MSG
- Organized structure: YYYY\MM_Month\filetype\
- Files moved after 30 minutes of inactivity
- Identical files skipped
- Newer files replace older ones
- Older files get versioned (filename_v1, v2, etc.)

### Documentation
- Complete README.md
- Step-by-step INSTALLATION_GUIDE.md
- requirements.txt for easy setup
- MIT License
- .gitignore for clean repository
- Batch file for easy startup
