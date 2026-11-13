@echo off
REM Renderiza a cena 3D na placa de video deste PC. Deixe cena.blend e ativar_gpu.py nesta mesma pasta.
REM Pode fechar e abrir de novo: continua de onde parou (nao refaz quadros prontos).
cd /d "%~dp0"
set B=%LOCALAPPDATA%\Microsoft\WindowsApps\blender-launcher.exe
if not exist "%B%" set B=blender
"%B%" -b "cena.blend" -P ativar_gpu.py -a
echo Pronto. Quadros na pasta "quadros".
pause
