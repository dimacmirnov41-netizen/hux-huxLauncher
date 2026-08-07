:: вот кому надо кто хочет сделать
@echo off
if exist dist rmdir /s /q dist
if exist hux-huxLauncher.build rmdir /s /q hux-huxLauncher.build
if exist hux-huxLauncher.onefile-build rmdir /s /q hux-huxLauncher.onefile-build

python -m nuitka --standalone --onefile --plugin-enable=tk-inter --jobs=12 --windows-uac-admin --windows-console-mode=disable --windows-icon-from-ico=icon.ico --include-data-files=hux.gif=hux.gif --include-data-files=icon.ico=icon.ico --output-filename="hux-huxLauncher" --output-dir=dist hux-huxLauncher.py

pause
