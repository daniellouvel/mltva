@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo  MLTVA - Nettoyage et Compilation Ciblee
echo ============================================

:: 1. Suppression des dossiers de build locaux
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: 2. Nettoyage du cache Nuitka dans AppData (Crucial !)
echo Nettoyage du cache systeme...
rd /s /q "%LocalAppData%\Nuitka\Nuitka\Cache" 2>nul

:: 3. Nettoyage des pycache locaux
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo.
echo Lancement de la compilation sur le fichier racine...
echo Fichier cible : %~dp0main.py
echo.

:: Utilisation de "%~dp0main.py" pour garantir qu'on compile le fichier de la racine
venv\Scripts\python.exe -m nuitka ^
    --standalone ^
    --enable-plugin=pyside6 ^
    --windows-console-mode=disable ^
    --output-filename=mltva.exe ^
    --output-dir=build ^
    --include-data-files=company.json=company.json ^
    --include-data-files=ui\style.qss=ui\style.qss ^
    --include-data-files=data\Logo.jpg=data\Logo.jpg ^
    --include-data-files=data\donne.png=data\donne.png ^
    --include-data-files=data\recoi.png=data\recoi.png ^
    --include-data-files=data\donne50.png=data\donne50.png ^
    --include-package=reportlab ^
    --noinclude-pytest-mode=nofollow ^
    --noinclude-setuptools-mode=nofollow ^
    --lto=no ^
    "%~dp0main.py"

if errorlevel 1 (
    echo [ERREUR] La compilation a echoue.
    pause & exit /b 1
)

:: 4. Creation du dossier final
mkdir dist\mltva
xcopy /e /i /y build\main.dist dist\mltva

:: Copie base de donnee
if not exist dist\mltva\data mkdir dist\mltva\data
copy data\mlbdd.db dist\mltva\data\mlbdd.db >nul

echo.
echo ============================================
echo  TERMINE ! L'exécutable est a jour.
echo ============================================
pause