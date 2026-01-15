# Poppler Setup for Windows

The PDF processing feature requires **Poppler** utilities to be installed on your system.

## Quick Install (Recommended)

### Option 1: Using Scoop (Easiest)
```powershell
# Install Scoop if you don't have it
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install Poppler
scoop install poppler
```

### Option 2: Manual Download
1. Download the latest release from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to `C:\poppler` (or any location)
3. Add `C:\poppler\Library\bin` to your system PATH

#### Adding to PATH:
1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "System variables", find and select "Path"
5. Click "Edit" → "New"
6. Add: `C:\poppler\Library\bin`
7. Click "OK" on all dialogs
8. **Restart your terminal/IDE**

## Verify Installation

Open a new terminal and run:
```powershell
pdftoppm -h
```

If you see help output, Poppler is correctly installed!

## Troubleshooting

If you still get errors after installation:
1. Make sure you've restarted your terminal/Streamlit app
2. Verify the PATH is set correctly: `$env:PATH -split ';' | Select-String poppler`
3. Check that `pdftoppm.exe` exists in the bin directory
