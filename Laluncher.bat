echo %cd%
cmd /k "activate maya && nuitka --onefile --windows-disable-console --output-dir=Launcher --follow-import-to=icons --standalone --enable-plugin=pyside2 Laluncher.py"