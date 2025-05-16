# -*- coding: utf-8 -*-

import ctypes
import os
import sys
import winreg

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "plugin"))


from flowlauncher import FlowLauncher

THEME_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"


class ToggleWindowsTheme(FlowLauncher):
    def query(self, query):
        return [
            {
                "Title": "Toggle Windows Theme (Light/Dark)",
                "SubTitle": "Press enter to toggle the Windows theme",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "toggle_windows_theme",
                    "parameters": [],
                },
            }
        ]

    def toggle_windows_theme(self):
        toggle_windows_theme()


def toggle_windows_theme():
    if is_dark_mode():
        enable_light_mode()
    else:
        enable_dark_mode()


def is_dark_mode():
    return get_reg("AppsUseLightTheme") == 0


def enable_dark_mode():
    set_theme(0)


def enable_light_mode():
    set_theme(1)


def set_theme(value):
    set_reg("AppsUseLightTheme", value)
    set_reg("SystemUsesLightTheme", value)
    broadcast_message("ImmersiveColorSet")


def get_reg(name):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, THEME_PATH) as key:
        value, _ = winreg.QueryValueEx(key, name)
        return value


def set_reg(name, value):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, THEME_PATH, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, value)
    winreg.CloseKey(key)


def broadcast_message(message):
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002

    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_SETTINGCHANGE,
        0,
        message,
        SMTO_ABORTIFHUNG,
        5000,  # Timeout in milliseconds
        None,
    )


if __name__ == "__main__":
    ToggleWindowsTheme()
