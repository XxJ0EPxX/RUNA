import os
import pygetwindow as gw

def open_application(app_name):
    app_paths = {
        "notepad": r"C:\Windows\System32\notepad.exe",
        "calculator": r"C:\Windows\System32\calc.exe",
        "paint": r"C:\Windows\System32\mspaint.exe",
        "wordpad": r"C:\Program Files\Windows NT\Accessories\wordpad.exe",
        "discord": r"C:\Users\Jesus\AppData\Local\Discord\app-1.0.9161\Discord.exe",
        "brave": r"C:\Users\Jesus\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe",
        "spotify": r"C:\Users\Jesus\AppData\Roaming\Spotify\Spotify.exe",
        "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        "access": r"C:\Program Files\Microsoft Office\root\Office16\MSACCESS.EXE",
        "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",

        # Añade aquí las rutas de más aplicaciones que quieras soportar
    }

    if app_name in app_paths:
        os.startfile(app_paths[app_name])
        return f"Abrí {app_name}."
    else:
        return f"No encontré la aplicación {app_name}."

def close_application(app_name):
    try:
        windows = gw.getWindowsWithTitle(app_name)
        if windows:
            for window in windows:
                window.close()
            return f"{app_name} ha sido cerrado."
        else:
            return f"No se encontró ninguna ventana de {app_name} abierta."
    except Exception as e:
        return f"No se pudo cerrar {app_name}. Error: {str(e)}"

