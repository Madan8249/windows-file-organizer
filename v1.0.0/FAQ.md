# Frequently Asked Questions (FAQ)

## General Questions

### Q1: What operating systems are supported?
**A:** Currently only Windows 10 and Windows 11 are supported.

### Q2: Does this work on Mac or Linux?
**A:** Not currently. The script uses Windows-specific paths and batch files. However, it could be adapted for Mac/Linux with minor modifications.

### Q3: Is this safe to use?
**A:** Yes! The script only moves files (doesn't delete) and includes duplicate detection to prevent data loss. However, always keep backups of important files.

### Q4: Can I see what files were moved?
**A:** Yes! Run the script manually with `python file_organizer.py` to see real-time output, or check the destination folders.

---

## Installation Questions

### Q5: Do I need to install Python?
**A:** Yes, Python 3.7 or higher is required. Follow the installation guide.

### Q6: Can I use Python 2?
**A:** No, Python 3.7+ is required due to dependencies and modern syntax.

### Q7: What is watchdog and why do I need it?
**A:** Watchdog is a Python library that monitors file system changes. It's essential for detecting new files.

### Q8: Installation failed, what should I do?
**A:** 
- Ensure you have admin rights
- Check internet connection
- Try: `pip install --upgrade watchdog`
- Verify Python is in PATH

---

## Configuration Questions

### Q9: Can I change the 30-minute delay?
**A:** Yes! Edit `file_organizer.py`, line 22:
```python
self.delay_minutes = 15  # Change to any number
```

### Q10: I don't have F: or D: drives. Can I change them?
**A:** Yes! Edit lines 212-213 in `file_organizer.py`:
```python
f_drive = "E:\\"  # Your drive
d_drive = "C:\\MyFolder\\"  # Can even be a folder
```

### Q11: Can I add more file types?
**A:** Yes! Edit lines 25-34 in `file_organizer.py`:
```python
self.file_types = {
    'docx': ['.docx', '.doc'],
    'videos': ['.mp4', '.avi', '.mkv'],  # Add this
    # Add more...
}
```

### Q12: Can I organize to network drives?
**A:** Yes, as long as the network drive is mapped and accessible. Use the mapped drive letter (e.g., `Z:\\`).

---

## Usage Questions

### Q13: How do I know if it's running?
**A:** Open Task Manager (Ctrl+Shift+Esc), go to Details tab, look for `pythonw.exe`.

### Q14: Can I run it manually instead of automatically?
**A:** Yes! Just run: `python file_organizer.py` in Command Prompt.

### Q15: How do I stop it?
**A:** 
- If running in CMD: Press Ctrl+C
- If running in background: Task Manager → End `pythonw.exe` process

### Q16: Will it organize files I already have in Downloads/Desktop?
**A:** No, by default it only organizes NEW files. To organize existing files, uncomment lines 235-239 in the script.

### Q17: What happens if I'm editing a file?
**A:** The timer resets every time you save/modify the file, so it won't move until 30 minutes AFTER you stop editing.

---

## File Handling Questions

### Q18: What happens to duplicate files?
**A:**
- **Identical files**: Skipped (deleted from source)
- **Newer files**: Replace the older version
- **Older files**: Saved as versioned (filename_v1.docx)

### Q19: Can I recover moved files?
**A:** Yes! They're not deleted, just moved. Check:
- F:\IN_MSG\YYYY\MM_Month\filetype\
- D:\OUT_MSG\YYYY\MM_Month\filetype\

### Q20: What about files being downloaded?
**A:** The script waits for 30 minutes, so incomplete downloads won't be moved. Plus, the timer resets if the file is still being written to.

### Q21: Will it move files from subfolders?
**A:** No, it only monitors the main Downloads and Desktop folders, not subfolders.

### Q22: What happens to files with no extension?
**A:** They go to the "others" folder.

---

## Troubleshooting Questions

### Q23: Script won't start - "Python not found"
**A:** 
- Reinstall Python with "Add to PATH" checked
- Or run: `setx PATH "%PATH%;C:\Python311"`

### Q24: "Module not found: watchdog"
**A:** Run: `pip install watchdog`

### Q25: Files aren't moving
**A:**
1. Check if F: and D: drives exist
2. Run manually to see error messages
3. Check file permissions
4. Verify the script is running (Task Manager)

### Q26: Script crashes immediately
**A:**
- Check drive letters in script match your system
- Run as Administrator
- Check Python version: `python --version`

### Q27: Auto-start doesn't work after restart
**A:**
- Verify batch file path is correct
- Check Startup folder: `Win+R` → `shell:startup`
- Or check Task Scheduler
- Ensure pythonw.exe (not python.exe) is used

### Q28: Getting permission errors
**A:**
- Run Command Prompt as Administrator
- Check folder permissions on destination drives
- Temporarily disable antivirus to test

---

## Advanced Questions

### Q29: Can I run multiple instances for different folders?
**A:** Yes, but you'll need to modify the script to monitor different folders and avoid conflicts.

### Q30: How can I see logs of what was moved?
**A:** Currently, run manually to see console output. Future versions will include log files.

### Q31: Can I schedule it to run only during work hours?
**A:** Not built-in, but you can use Task Scheduler to start/stop the script at specific times.

### Q32: Will this slow down my computer?
**A:** No, it uses minimal resources. The watchdog library is very efficient.

### Q33: Can I exclude certain files or folders?
**A:** Yes, modify the `organize_file()` function to add exclusion logic:
```python
if "donotmove" in filename.lower():
    return  # Skip this file
```

---

## Performance Questions

### Q34: How many files can it handle?
**A:** Thousands. It processes files one at a time with minimal memory usage.

### Q35: Does it work with large files (videos, ISOs)?
**A:** Yes! It moves files regardless of size. However, moving very large files may take time.

### Q36: Will it work if my computer sleeps?
**A:** The timers pause during sleep. When the computer wakes, timers resume from where they left off.

---

## Security & Privacy Questions

### Q37: Does this script send any data online?
**A:** No! It operates completely offline. No data is sent anywhere.

### Q38: Can I review the code?
**A:** Absolutely! The entire source code is open and available in `file_organizer.py`.

### Q39: Is my data safe?
**A:** Yes, files are moved (not copied then deleted), preserving all metadata and permissions.

---

## Future Features

### Q40: Will there be a GUI?
**A:** It's planned for future versions!

### Q41: Can you add email notifications?
**A:** This is on the roadmap for v2.0.

### Q42: Will it support cloud storage (Dropbox, OneDrive)?
**A:** Potentially in future versions if there's demand.

---

## Getting Help

### Q43: Where can I report bugs?
**A:** Open an issue on the GitHub repository with details about the bug.

### Q44: How can I request features?
**A:** Create a feature request issue on GitHub.

### Q45: Can I contribute to the project?
**A:** Yes! See CONTRIBUTING.md for guidelines.

---

**Still have questions?** Open an issue on GitHub!
