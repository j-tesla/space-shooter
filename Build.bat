@echo off
:: clean up previous build
del /f /s /q main.spec >nul 2>&1
del /f /s /q build >nul 2>&1
del /f /s /q dist >nul 2>&1
rmdir /q /s build
rmdir /q /s dist

:: check if pip exists because we're gonna build in pipenv.
where /q pip
IF ERRORLEVEL 1 (
    ECHO pip is missing. please install it from https://pip.pypa.io/en/stable/installing/# .
    EXIT /B
) 

:: check and download dependencies.
echo ==== checking dependencies
pip install PyInstaller pygame pywin32 pipenv
pipenv install

:: Build.
:: Note: if you have issues with .ogg or .wav files failing load
:: check this issue out: https://github.com/pygame/pygame/issues/1514
echo ==== starting build
pipenv run pyinstaller main.py --noconfirm ^
	--onefile  ^
    --add-data="resources;resources" ^
	--add-data="README.md;." ^
	--add-data="resources;resources"

