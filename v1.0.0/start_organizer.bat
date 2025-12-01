@echo off
REM Windows File Organizer - Startup Script
REM This script starts the file organizer in the background

echo Starting File Organizer...
start /min pythonw "C:\FileOrganizer\file_organizer.py"

REM Check if started successfully
timeout /t 2 /nobreak >nul
tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo File Organizer started successfully!
) else (
    echo Error: File Organizer failed to start
    pause
)
