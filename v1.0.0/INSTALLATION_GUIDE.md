# Installation Guide - Windows File Organizer

Complete step-by-step installation guide for Windows 10/11.

## 📋 Prerequisites

- Windows 10 or Windows 11
- Administrator access
- Internet connection (for downloading Python)
- F: and D: drives (or modify script for your drives)

## 🔧 Detailed Installation Steps

### Step 1: Install Python (5 minutes)

#### 1.1 Download Python
1. Open your web browser
2. Navigate to: https://www.python.org/downloads/
3. Click **"Download Python 3.x.x"** (yellow button)
4. Save the installer to your Downloads folder

#### 1.2 Run Python Installer
1. Double-click the downloaded file (e.g., `python-3.11.x-amd64.exe`)
2. ⚠️ **CRITICAL**: Check ☑️ **"Add Python to PATH"**
3. Click **"Install Now"**
4. Wait for installation (2-3 minutes)
5. Click **"Close"** when finished

#### 1.3 Verify Python Installation
1. Press `Win + R`
2. Type `cmd` and press Enter
3. In the command window, type: `python --version`
4. You should see: `Python 3.x.x`
5. Type: `exit` and press Enter

✅ Python is installed!

---

### Step 2: Install Watchdog Library (2 minutes)

#### 2.1 Open Command Prompt as Admin
1. Press `Win + X`
2. Select **"Terminal (Admin)"** or **"Command Prompt (Admin)"**
3. Click **"Yes"** when prompted

#### 2.2 Install Watchdog
In the admin command window, type:
```bash
pip install watchdog
```
Press Enter and wait (30-60 seconds)

You should see: `Successfully installed watchdog-3.0.0`

✅ Watchdog library installed!

---

### Step 3: Download and Setup Script (3 minutes)

#### 3.1 Create Project Folder
1. Press `Win + E` to open File Explorer
2. Navigate to `C:\`
3. Right-click → New → Folder
4. Name it: `FileOrganizer`

#### 3.2 Download Files
1. Download all files from the GitHub repository
2. Extract/Copy these files to `C:\FileOrganizer\`:
   - `file_organizer.py`
   - `requirements.txt`
   - `README.md`
   - `INSTALLATION_GUIDE.md`

#### 3.3 Alternative: Clone with Git
If you have Git installed:
```bash
cd C:\
git clone https://github.com/soren-code/windows-file-organizer.git FileOrganizer
cd FileOrganizer
pip install -r requirements.txt
```

---

### Step 4: Configure (Optional - 2 minutes)

#### 4.1 Check Drive Letters
Open File Explorer and verify:
- F: drive exists
- D: drive exists

#### 4.2 Modify Script (if needed)
If your drives are different:
1. Right-click `file_organizer.py` → Edit with Notepad
2. Find lines 212-213:
```python
f_drive = "F:\\"  # Change this
d_drive = "D:\\"  # Change this
```
3. Change to your drive letters (e.g., `"G:\\"`, `"E:\\"`)
4. Save and close

#### 4.3 Change Delay Time (optional)
Find line 22:
```python
self.delay_minutes = 30  # Change to 15, 60, etc.
```

---

### Step 5: Test Run (2 minutes)

#### 5.1 Manual Test
1. Press `Win + R`
2. Type `cmd` and press Enter
3. Type: `cd C:\FileOrganizer`
4. Press Enter
5. Type: `python file_organizer.py`
6. Press Enter

#### 5.2 Expected Output
You should see:
