ECHO OFF
cls

ECHO ===============================================
ECHO Choose an option...
ECHO ===============================================
ECHO 1, build
ECHO 2, install requirements
ECHO 3, install requirements and build
ECHO ===============================================
ECHO Using venv...
ECHO ===============================================
ECHO 4, build
ECHO 5, install requirements
ECHO 6, install requirements and build
ECHO 7, setup the enviroment
CHOICE /C:1234567
IF ERRORLEVEL 7 GOTO Vsu
IF ERRORLEVEL 6 GOTO Vrb
IF ERRORLEVEL 5 GOTO VIr
IF ERRORLEVEL 4 GOTO Vb
IF ERRORLEVEL 3 GOTO Rb
IF ERRORLEVEL 2 GOTO Ir
IF ERRORLEVEL 1 GOTO B

:B
cls
pyinstaller --add-data "json/*.json;json" --add-data "font/*.ttf;font" --add-data "icon/*.ico;icon" --add-data "exe/*.exe;exe" --noconsole --onefile --noconfirm -i "icon/icon.ico" ytdldpg.py
GOTO End

:Ir
cls
pip install -r requirements.txt
GOTO End

:Rb
cls
pip install -r requirements.txt
pyinstaller --add-data "json/*.json;json" --add-data "font/*.ttf;font" --add-data "icon/*.ico;icon" --add-data "exe/*.exe;exe" --noconsole --onefile --noconfirm -i "icon/icon.ico" ytdldpg.py
GOTO End

:Vb
cls
call ./venv/Scripts/activate.bat
pyinstaller --add-data "json/*.json;json" --add-data "font/*.ttf;font" --add-data "icon/*.ico;icon" --add-data "exe/*.exe;exe" --noconsole --onefile --noconfirm -i "icon/icon.ico" ytdldpg.py
GOTO VEnd

:Vir
cls
call ./venv/Scripts/activate.bat
pip install -r requirements.txt
GOTO VEnd

:Vrb
cls
call ./venv/Scripts/activate.bat
pip install -r requirements.txt
pyinstaller --add-data "json/*.json;json" --add-data "font/*.ttf;font" --add-data "icon/*.ico;icon" --add-data "exe/*.exe;exe" --noconsole --onefile --noconfirm -i "icon/icon.ico" ytdldpg.py
GOTO VEnd

:Vsu
cls
ECHO Please wait while python creates the enviroment this may take a moment...
mkdir .\venv
py -m venv ./venv
ECHO Finished
GOTO End

:VEnd
call ./venv/Scripts/deactivate.bat

:End
pause
