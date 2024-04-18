import winreg

def check_password_history(expected_history_size=24):  # Adding a parameter here
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
        password_history_size, _ = winreg.QueryValueEx(key, "PasswordHistorySize") 

        if password_history_size >= expected_history_size:
            return "PASS" 
        else:
            return "FAIL"

    except FileNotFoundError:
        return "KEY_NOT_FOUND"

def check_maximum_password_age(expected_max_age=365):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
        maximum_password_age, _ = winreg.QueryValueEx(key, "MaximumPasswordAge") 

        if 1 <= maximum_password_age <= expected_max_age:
            return "PASS"
        else:
            return "FAIL"

    except FileNotFoundError:
        return "KEY_NOT_FOUND"

def check_password_complexity():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
        password_complexity, _ = winreg.QueryValueEx(key, "PasswordComplexity") 

        if password_complexity == 1: 
            return "PASS"
        else:
            return "FAIL"

    except FileNotFoundError:
        return "KEY_NOT_FOUND"