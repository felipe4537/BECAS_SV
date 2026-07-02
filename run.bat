@echo off
title BECAS_SV - Sistema de Monitoreo
echo ====================================
echo  BECAS_SV - Verificando dependencias
echo ====================================
pip install flask openpyxl
echo.
echo ====================================
echo  PASO IMPORTANTE:
echo  Si es la primera vez, ejecuta:
echo    python migrar_sqlite.py
echo  para crear BECAS_SV.db desde SQL Server
echo ====================================
echo  Iniciando servidor...
echo  Abre http://127.0.0.1:5000
echo ====================================
python app.py
pause
