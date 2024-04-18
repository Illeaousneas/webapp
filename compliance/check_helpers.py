import winreg

def check_guest_account_status():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
        value, _ = winreg.QueryValueEx(key, "GuestAccountStatus") 

        if value == 1: 
            return "PASS"
        else:
            return "FAIL"

    except FileNotFoundError:
        return "KEY_NOT_FOUND" 
