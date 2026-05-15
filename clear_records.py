"""
Clear Windows SRU Records Utility
---------------------------------

Purpose:
    This script clears/resets Windows network data usage records by safely
    backing up the SRUDB.dat file located inside:

        C:\Windows\System32\sru\SRUDB.dat

    Windows stores network/data usage information in this database file.
    Since the file is normally locked while Windows is running, this script
    temporarily stops the DPS service, moves SRUDB.dat to a backup file, and
    then starts the DPS service again.

What this script does:
    1. Creates a temporary batch file.
    2. Requests Administrator permission using Windows UAC.
    3. Stops the DPS service.
    4. Checks whether SRUDB.dat exists.
    5. Moves SRUDB.dat to SRUDB.dat.bak.
       - If SRUDB.dat.bak already exists, it is overwritten.
    6. Starts the DPS service again.
    7. Saves operation details in a log file inside the Windows TEMP folder.

Important:
    - Administrator permission is required.
    - A Windows UAC popup will appear.
    - This script does not permanently delete SRUDB.dat directly.
      It renames/moves it to SRUDB.dat.bak.
    - Windows may recreate SRUDB.dat automatically after the DPS service starts.
    - The script always attempts to restart the DPS service, even if the move
      operation fails.

Log file:
    The log file is created here:

        %TEMP%\clear_sru_log.txt

Use case:
    Use this when you want to reset Windows data usage records safely from
    a Python script while keeping a backup of the original SRUDB.dat file.

Author:
    TutorialsAndroid

File:
    clear_records.py
"""
import ctypes
import tempfile
import os
from ctypes import wintypes

SEE_MASK_NOCLOSEPROCESS = 0x00000040
SW_SHOW = 1
INFINITE = 0xFFFFFFFF

class SHELLEXECUTEINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("fMask", wintypes.ULONG),
        ("hwnd", wintypes.HWND),
        ("lpVerb", wintypes.LPCWSTR),
        ("lpFile", wintypes.LPCWSTR),
        ("lpParameters", wintypes.LPCWSTR),
        ("lpDirectory", wintypes.LPCWSTR),
        ("nShow", ctypes.c_int),
        ("hInstApp", wintypes.HINSTANCE),
        ("lpIDList", wintypes.LPVOID),
        ("lpClass", wintypes.LPCWSTR),
        ("hkeyClass", wintypes.HKEY),
        ("dwHotKey", wintypes.DWORD),
        ("hIcon", wintypes.HANDLE),
        ("hProcess", wintypes.HANDLE),
    ]

def run_bat_as_admin_and_wait(bat_path):
    sei = SHELLEXECUTEINFO()
    sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFO)
    sei.fMask = SEE_MASK_NOCLOSEPROCESS
    sei.hwnd = None
    sei.lpVerb = "runas"
    sei.lpFile = "cmd.exe"
    sei.lpParameters = f'/c "{bat_path}"'
    sei.lpDirectory = None
    sei.nShow = SW_SHOW

    success = ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei))

    if not success:
        return False, "UAC cancelled or failed to start"

    ctypes.windll.kernel32.WaitForSingleObject(sei.hProcess, INFINITE)

    exit_code = wintypes.DWORD()
    ctypes.windll.kernel32.GetExitCodeProcess(sei.hProcess, ctypes.byref(exit_code))
    ctypes.windll.kernel32.CloseHandle(sei.hProcess)

    if exit_code.value == 0:
        return True, "Success"
    else:
        return False, f"Failed with exit code {exit_code.value}"


def create_clear_records_bat():
    log_path = os.path.join(tempfile.gettempdir(), "clear_sru_log.txt")

    bat_content = rf'''
@echo off
setlocal

set "SRU_FILE=C:\Windows\System32\sru\SRUDB.dat"
set "BAK_FILE=C:\Windows\System32\sru\SRUDB.dat.bak"
set "LOG_FILE={log_path}"

echo Starting SRU clear process... > "%LOG_FILE%"

echo Stopping DPS service... >> "%LOG_FILE%"
net stop DPS >> "%LOG_FILE%" 2>&1

timeout /t 2 /nobreak >nul

if not exist "%SRU_FILE%" (
    echo SRUDB.dat not found. >> "%LOG_FILE%"
    set "STATUS=2"
    goto START_DPS
)

echo Moving SRUDB.dat to backup... >> "%LOG_FILE%"
move /Y "%SRU_FILE%" "%BAK_FILE%" >> "%LOG_FILE%" 2>&1
set "STATUS=%ERRORLEVEL%"

:START_DPS
echo Starting DPS service... >> "%LOG_FILE%"
net start DPS >> "%LOG_FILE%" 2>&1

echo Finished with status %STATUS%. >> "%LOG_FILE%"
exit /b %STATUS%
'''

    bat_path = os.path.join(tempfile.gettempdir(), "clear_sru_records.bat")

    with open(bat_path, "w", encoding="utf-8") as file:
        file.write(bat_content)

    return bat_path, log_path


if __name__ == "__main__":
    bat_path, log_path = create_clear_records_bat()

    success, message = run_bat_as_admin_and_wait(bat_path)

    print(message)
    print("Log file:", log_path)

    if success:
        print("DPS stopped, SRUDB.dat backed up, and DPS started again.")
    else:
        print("Something failed. Check the log file for details.")