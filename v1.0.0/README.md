# Windows File Organizer 🗂️

Automatically organize files from Downloads and Desktop folders into structured directories with a 30-minute delay.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 📋 Overview

This script automatically monitors your Downloads and Desktop folders and organizes files into structured directories based on:
- Year (2025, 2026, etc.)
- Month (01_January, 02_February, etc.)
- File type (docx, xlsx, pdf, jpg, png, etc.)

Files are moved **30 minutes** after creation or last modification, giving you time to work on them.

## ✨ Features

- ⏱️ **30-Minute Delay**: Files move only after 30 minutes of inactivity
- 📁 **Auto-Organization**: Structured by Year/Month/FileType
- 🔄 **Smart Duplicates**: Replaces newer files, versions older ones
- 🚀 **Auto-Start**: Runs automatically at Windows startup
- 🎯 **Multiple File Types**: Supports docx, xlsx, pdf, jpg, png, txt, pptx, zip, mp4, mp3, and more
- 💾 **Safe**: Checks file hashes to prevent data loss

## 📂 Folder Structure
