echo %cd%
rmdir /s /q build
rmdir /s /q dist
start cmd /k "pyinstaller Laluncher_ui.spec"