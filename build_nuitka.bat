@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo  Compilation MLTVA avec Nuitka
echo ============================================

:: Verification Nuitka
venv\Scripts\python.exe -m nuitka --version >nul 2>&1
if errorlevel 1 (
    echo Nuitka non trouve. Installation...
    venv\Scripts\pip.exe install nuitka
    if errorlevel 1 (
        echo ERREUR : impossible d'installer Nuitka.
        pause & exit /b 1
    )
)

:: Nettoyage builds precedents
if exist build rmdir /s /q build
if exist dist\mltva rmdir /s /q dist\mltva

echo.
echo Compilation en cours (peut prendre 20 a 30 minutes)...
echo.

venv\Scripts\python.exe -m nuitka ^
    --standalone ^
    --enable-plugin=pyside6 ^
    --windows-console-mode=disable ^
    --output-filename=mltva.exe ^
    --output-dir=build ^
    --include-data-files=data\Logo.jpg=data\Logo.jpg ^
    --include-data-files=data\donne.png=data\donne.png ^
    --include-data-files=data\recoi.png=data\recoi.png ^
    --include-data-files=data\donne50.png=data\donne50.png ^
    --include-package=reportlab ^
    --noinclude-pytest-mode=nofollow ^
    --noinclude-setuptools-mode=nofollow ^
    main.py

if errorlevel 1 (
    echo.
    echo ERREUR : La compilation a echoue.
    pause & exit /b 1
)

:: Copier le resultat dans dist\mltva
mkdir dist\mltva
xcopy /e /i /q build\main.dist dist\mltva

:: Creer le dossier data avec la base de donnees dans dist
if not exist dist\mltva\data mkdir dist\mltva\data
copy data\mlbdd.db dist\mltva\data\mlbdd.db >nul

:: Nettoyage build intermediaire
rmdir /s /q build

echo.
echo ============================================
echo  Termine !
echo  Application : dist\mltva\mltva.exe
echo ============================================
echo.
echo Pour distribuer : copier tout le dossier dist\mltva\
echo La base de donnees est dans dist\mltva\data\
echo.
pause
endlocal
