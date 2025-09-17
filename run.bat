@echo off
REM Ir al directorio del proyecto
cd /d "E:\Proyecto Porfolio\Gestor Alimentos"

REM Activar entorno virtual
call .\venv\Scripts\activate

REM Iniciar FastAPI en segundo plano
start uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

REM Esperar unos segundos a que arranque FastAPI
timeout /t 3 >nul

REM Iniciar ngrok en el puerto 8000
start ngrok http 8000

REM Esperar a que ngrok cree el túnel
timeout /t 5 >nul

REM Usar PowerShell para sacar la primera URL pública con https
for /f "delims=" %%i in ('powershell -NoProfile -Command ^
    "(Invoke-RestMethod http://127.0.0.1:4040/api/tunnels).tunnels | Where-Object { $_.public_url -like 'https*' } | Select-Object -ExpandProperty public_url -First 1"') do (
    set NGROK_URL=%%i
)

echo.
echo Tu API está disponible en: %NGROK_URL%

pause
