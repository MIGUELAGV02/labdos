@echo off
chcp 65001 > nul
title UTVT - Taller de Copilot y Laboratorios 1 al 7

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py "%~dp0ejecutar_laboratorios.py"
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python "%~dp0ejecutar_laboratorios.py"
    goto end
)

echo [ERROR] No se encontro Python instalado ni el launcher 'py'.
echo Por favor asegurese de tener Python en el PATH del sistema.
pause

:end
