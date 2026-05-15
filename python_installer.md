# GenFlooder v2 - Build Guide

This guide explains how to build the main application EXE and the uninstaller EXE using PyInstaller.

---

## Requirements

Make sure Python is installed and added to PATH.

Install PyInstaller:

```bash
pip install pyinstaller
````

Check PyInstaller installation:

```bash
python -m PyInstaller --version
```

---

## Project Files

Your project should look like this:

```text
project-folder/
│
├── GenFlooder_v2.py
├── remove_autostart.py
|-- clear_records.py
├── icons/
|----- icon.ico
|----- uni_icon.ico    
└── README.md
```

| File                  | Purpose                                   |
| --------------------- | -----------------------------------       |
| `Gen_v2.py`           | Main application file                     |
| `remove_autostart.py` | Uninstaller / remove autostart file       |
| `clear_records.py`    | clears/resets Windows network data usage  |
| `icon.ico`            | Icon for main app                         |
| `uni_icon.ico`        | Icon for uninstaller                      |

---

# Build Main App / Installer

This command builds the main application as a single EXE file.

```bash
python -m PyInstaller --onefile --noconsole --icon=icons/icon.ico --name regx GenFlooder_v2.py
```

Output file:

```text
dist/regx.exe
```

### What this does

* Creates a single `.exe` file
* Hides the terminal window
* Adds the custom app icon
* Names the final app `regx.exe`

Use this build for the final background-running app.

---

# Build Main App With Console

Use this version only for testing or debugging.

```bash
python -m PyInstaller --onefile --icon=icons/icon.ico --name regxdebug GenFlooder_v2.py
```

Output file:

```text
dist/regxdebug.exe
```

This version will show a terminal window when the app runs.

---

# Build Uninstaller

This command builds the uninstaller EXE.

```bash
python -m PyInstaller --onefile --icon=icons/uni_icon.ico --name uninstall remove_autostart.py
```

Output file:

```text
dist/uninstall.exe
```

### What this does

* Creates a single uninstaller `.exe`
* Adds the uninstaller icon
* Names the final file `uninstall.exe`
* Removes the app from Windows startup, depending on your `remove_autostart.py` logic

# Clear Network Data Usage Records

When we run regx.exe or GenFlooder_v2.py it sends UDP packets to default gateway. So in the windows
network usage we can see the application name regx.exe or GenFlooder_v2.py sending lot of data and 
it will look fishy if anyone found that network usage. So with the help of clear_records.py or clear.exe
we will wipe out / reset the windows network data usage.

This command build the installer EXE

```bash
python -m PyInstaller --onefile --icon=icons/clean.ico --name="Reset Data" clear_records.py
```

---

# Recommended Build Commands

For final release, run these two commands:

```bash
python -m PyInstaller --onefile --noconsole --icon=icons/icon.ico --name regx GenFlooder_v2.py
```

```bash
python -m PyInstaller --onefile --icon=icons/uni_icon.ico --name uninstall remove_autostart.py
```

After building, copy these files from the `dist` folder:

```text
dist/regx.exe
dist/uninstall.exe
```

---

# Output Folder

After building, PyInstaller creates these folders and files:

```text
project-folder/
│
├── build/
├── dist/
│   ├── regx.exe
│   └── uninstall.exe
│
├── regx.spec
├── uninstall.spec
```

The final EXE files are inside the `dist` folder.

---

# Clean Build Files

To remove old build files before rebuilding, delete:

```text
build/
dist/
regx.spec
uninstall.spec
```

Then run the build commands again.

---

# Important Notes

* `--onefile` creates a single EXE file.
* `--noconsole` hides the terminal window.
* `--icon=icon.ico` sets the EXE icon.
* `--name regx` sets the main app EXE name.
* `--name uninstall` sets the uninstaller EXE name.
* The main app should use `--noconsole` if it runs in the background.
* The uninstaller can be built with console enabled so users can see removal messages.

---

# Testing

After building:

1. Run `regx.exe` once.
2. Check if it adds itself to Windows startup.
3. Restart Windows or log out and log in again.
4. Confirm the app runs automatically.
5. Run `uninstall.exe`.
6. Confirm the app is removed from Windows startup.

---

# Example

Final release files:

```text
regx.exe
uninstall.exe
```

You can share both files together:

```text
regx/
│
├── regx.exe
└── uninstall.exe
```

```
```
