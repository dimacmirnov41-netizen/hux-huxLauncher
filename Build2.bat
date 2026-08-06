:: вот кому надо кто хочет сделать
@echo off
if exist dist rmdir /s /q dist
python -m PyInstaller --clean --noconsole --onefile --uac-admin --name "hux-huxLauncher" --icon=icon.ico --add-data "hux.gif;." hux-huxLauncher.py
if exist build rmdir /s /q build
if exist hux-huxLauncher.spec del /f /q hux-huxLauncher.spec
pause
