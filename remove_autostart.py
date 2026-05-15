import winreg

APP_NAME = "regx"

def remove_from_startup():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            key_path,
            0,
            winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, APP_NAME)

        print("Removed from startup successfully.")

    except FileNotFoundError:
        print("App was not found in startup.")


remove_from_startup()