# Changelog

All notable changes to this project will be documented in this file.

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

## [Unreleased]

### Planned Features
- Configuration file (config.ini) for easier customization
- GUI for settings management
- Email notifications when files are moved
- Statistics dashboard
- Support for network drives
- Custom rules for specific file types
- Exclude folders option
- Multiple source/destination pairs
- Schedule-based organization (work hours only)
