@echo off
echo Iniciando Conversor TIFF para DICOM (pylinac)...
echo.
cd /d "%~dp0"

REM Verificar se pylinac está instalado
.venv\Scripts\python.exe -c "import pylinac" 2>nul
if errorlevel 1 (
    echo AVISO: pylinac nao esta instalado!
    echo.
    echo Instalando pylinac...
    .venv\Scripts\pip.exe install pylinac
    echo.
    if errorlevel 1 (
        echo.
        echo ERRO: Falha ao instalar pylinac.
        echo Por favor, instale manualmente:
        echo .venv\Scripts\pip.exe install pylinac
        echo.
        pause
        exit /b 1
    )
)

.venv\Scripts\pythonw.exe tiff_to_dicom_gui.py
if errorlevel 1 (
    echo.
    echo Erro ao executar. Tentando com python.exe...
    .venv\Scripts\python.exe tiff_to_dicom_gui.py
    pause
)
