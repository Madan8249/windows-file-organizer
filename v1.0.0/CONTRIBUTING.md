# Contributing to Windows File Organizer

Thank you for considering contributing to this project! 

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your Windows version and Python version
   - Error messages (if any)

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use case / why it would be useful
   - Possible implementation ideas

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly on Windows 10/11
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions
- Keep functions focused and small

### Testing

Before submitting:
- Test on Windows 10 and/or Windows 11
- Test with different file types
- Test duplicate handling scenarios
- Test with missing drives
- Verify auto-start functionality

### Documentation

- Update README.md if adding features
- Update INSTALLATION_GUIDE.md if changing setup
- Add entries to CHANGELOG.md
- Comment your code clearly

## Development Setup
```bash
# Clone your fork
git clone https://github.com/Madan8249/windows-file-organizer.git
cd windows-file-organizer

# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest

# Run the script
python file_organizer.py
```

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## Questions?

Feel free to open an issue for any questions!

Thank you for contributing! 🎉
