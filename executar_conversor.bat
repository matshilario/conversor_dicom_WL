@echo off
echo Iniciando Conversor DICOM .img...
echo.
cd /d "%~dp0"
.venv\Scripts\pythonw.exe dicom_converter_gui.py
if errorlevel 1 (
    echo.
    echo Erro ao executar. Pressione qualquer tecla para tentar com python.exe...
    pause >nul
    .venv\Scripts\python.exe dicom_converter_gui.py
    pause
)
