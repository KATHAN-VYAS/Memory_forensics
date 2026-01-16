# Memory Forensics Toolkit

A Python-based memory and storage forensics toolkit for creating disk images and recovering deleted data.  This project was originally developed as a personal project and later integrated into the ForenSight project.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [RAW Image Creation](#raw-image-creation)
  - [Data Recovery](#data-recovery)
- [Examples](#examples)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🔍 Overview

This toolkit provides two main functionalities:

1. **RAW Imaging (`RAWimg.py`)**: Create forensically sound RAW images of storage devices with cryptographic hash verification
2. **Data Recovery (`Recover.py`)**: Recover deleted JPG files from storage devices by scanning for JPEG file signatures

## ✨ Features

### RAWimg.py
- Create bit-by-bit RAW images of storage devices
- Support for multiple hash algorithms (MD5, SHA256)
- Detailed logging for forensic audit trails
- Cross-platform path conversion (Windows/Cygwin)
- Error handling with sync and noerror options
- Configurable block sizes for optimal performance

### Recover.py
- Recover deleted JPG files from raw storage devices
- Scans for JPEG file signatures (`0xFFD8FFE0`)
- Extracts complete JPEG files
- Sequential file naming for recovered images

## 📦 Prerequisites

### System Requirements

- **Operating System**: Windows (with Cygwin for RAWimg.py)
- **Python**: Python 3.6 or higher
- **Administrator/Root Privileges**: Required for raw disk access

### Required Software

#### For RAWimg.py:
1. **Cygwin** (Windows only)
   - Required for the `dd` command
   - Must include the `dd` utility package

#### For Recover.py:
- No additional software required beyond Python

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/KATHAN-VYAS/Memory_forensics.git
cd Memory_forensics
```

### Step 2: Install Python Dependencies

Both scripts use Python standard library modules, so no external packages need to be installed via pip.

**Dependencies used:**
- `subprocess` (built-in)
- `hashlib` (built-in)
- `argparse` (built-in)
- `os` (built-in)
- `sys` (built-in)
- `logging` (built-in)

### Step 3: Install Cygwin (For RAWimg.py on Windows)

1. Download Cygwin from [https://www.cygwin.com/](https://www.cygwin.com/)
2. Run the installer
3. During package selection, ensure you install: 
   - `coreutils` (contains `dd`)
4. Default installation path:  `C:\cygwin64\`
5. If you install to a different path, update the path in `RAWimg.py` at line 145: 
   ```python
   create_image(args.source, args.output, args.block_size, r"C:\cygwin64\bin\bash.exe")
   ```

### Step 4: Verify Installation

#### Test RAWimg.py:
```bash
python RAWimg.py --help
```

#### Test Recover.py:
```bash
python Recover.py
```

## 📖 Usage

### RAW Image Creation

#### Basic Syntax

```bash
python RAWimg.py -s <source_device> -o <output_file> [OPTIONS]
```

#### Required Arguments

- `-s, --source`: Source device path (e.g., `/dev/sda` on Linux, `\\.\PhysicalDrive0` on Windows)
- `-o, --output`: Output image file path

#### Optional Arguments

- `-b, --block-size`: Block size for dd operation (default: `4M`)
- `-t, --hash-type`: Hash algorithm - `md5` or `sha256` (default: `sha256`)
- `-l, --log`: Log file path (default: `imaging.log`)

#### Example Commands

**Create a basic RAW image:**
```bash
python RAWimg.py -s \\.\D: -o D:\forensics\evidence.raw
```

**Create image with MD5 hash:**
```bash
python RAWimg.py -s \\.\PhysicalDrive1 -o C:\images\drive1.raw -t md5
```

**Custom block size and log file:**
```bash
python RAWimg.py -s \\.\E: -o E:\backup. raw -b 8M -l custom.log
```

### Data Recovery

#### Basic Usage

The `Recover.py` script is configured to scan a specific drive.  You need to modify the script before running. 

#### Step 1: Edit the Drive Letter

Open `Recover.py` and modify line 3: 

```python
drive = r"\\.\D:"  # Change D: to your target drive letter
```

#### Step 2: Run the Script

```bash
python Recover.py
```

#### Step 3: Recovered Files

- Recovered JPG files will be saved in the current directory
- Files are named sequentially: `0.jpg`, `1.jpg`, `2.jpg`, etc.

#### Important Notes for Data Recovery

⚠️ **Warning**: 
- Run with administrator privileges
- The drive should be unmounted or in read-only mode
- Do NOT write recovered files to the same drive being scanned
- Use a write-blocker for forensic investigations

## 💡 Examples

### Example 1: Create Forensic Image of USB Drive

```bash
# Identify drive (Windows)
wmic diskdrive list brief

# Create image with SHA256 hash
python RAWimg.py -s \\.\PhysicalDrive2 -o E:\forensics\usb_evidence.raw -t sha256 -l usb_imaging.log
```

### Example 2: Recover Deleted Photos

```python
# Edit Recover.py
drive = r"\\.\F:"  # SD card drive

# Run recovery
python Recover.py

# Output: 
# ==== Found JPG at location: 0x1a400 ====
# ==== Wrote JPG to location: 0.jpg ====
# ... 
```

### Example 3: Create Image with Custom Parameters

```bash
python RAWimg.py \
  -s \\.\PhysicalDrive1 \
  -o D:\cases\case_2024_001\evidence.raw \
  -b 16M \
  -t sha256 \
  -l case_2024_001.log
```

## 📝 Logging

### RAWimg.py Logging

The script generates detailed logs including:
- Start/end timestamps
- Source and destination paths
- Block size and hash type
- Cygwin path conversions
- dd command execution
- Hash calculation results
- Error messages

**Log Format:**
```
2026-01-16 14:30:00 - INFO - RAW Image Creation Script Started. 
2026-01-16 14:30:01 - INFO - Starting imaging process: \\.\D: -> D:\image. raw with block-size: 4M
2026-01-16 14:35:22 - INFO - Imaging completed successfully.
2026-01-16 14:35:23 - INFO - SHA256 hash:  abc123def456... 
2026-01-16 14:35:24 - INFO - Hash saved to D:\image.raw. sha256
2026-01-16 14:35:24 - INFO - Process completed successfully.
```

### Recover.py Output

Console output shows:
- Location of found JPG files (hex offset)
- Names of recovered files
- Progress updates

## 🔧 Troubleshooting

### Common Issues

#### 1. "Cygwin bash not found"

**Error:**
```
ERROR - Cygwin bash not found at C:\cygwin64\bin\bash.exe
```

**Solution:**
- Install Cygwin
- Update the path in `RAWimg.py` line 145 to match your installation

#### 2. "Source device does not exist"

**Error:**
```
ERROR - Source device \\.\D: does not exist. 
```

**Solution:**
- Verify the device path
- Run as Administrator
- Use `wmic diskdrive list brief` to list available drives

#### 3. Permission Denied

**Error:**
```
ERROR - Source device is not readable.  Check permissions.
```

**Solution:**
- Run Command Prompt/Terminal as Administrator
- Check if drive is locked or in use

#### 4. No JPG Files Recovered

**Problem:** Recover.py runs but finds no files

**Solution:**
- Verify the drive letter is correct
- Ensure the drive hasn't been overwritten
- Check that files were actually JPG format
- Try scanning a different drive or partition

#### 5. Python Not Recognized

**Error:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
- Install Python 3.6+
- Add Python to system PATH
- Use `python3` instead of `python`

## ⚖️ Legal and Ethical Use

**IMPORTANT**: This toolkit is designed for: 
- Legitimate forensic investigations
- Data recovery from your own devices
- Educational purposes
- Authorized security research

**DO NOT USE** for:
- Unauthorized access to systems or data
- Illegal data recovery
- Violating privacy laws
- Any unethical purposes

Always ensure you have proper authorization before performing forensic operations on any device.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Contact

For questions or support, please open an issue on GitHub. 

## 🙏 Acknowledgments

This project was part of the ForenSight project and serves as a practical implementation of digital forensics techniques.

---

**Note**: This toolkit is provided as-is for educational and legitimate forensic purposes. Always follow applicable laws and regulations when performing digital forensics. 
