@echo off
echo ===============================================
echo    SOLUCION RAPIDA PARA PYTHON 3.13
echo ===============================================
echo.

echo Instalando setuptools primero...
pip install setuptools wheel

echo Instalando paquetes precompilados...
pip install streamlit==1.28.0
pip install numpy==1.24.3 --only-binary=all
pip install pandas==2.0.3 --only-binary=all
pip install plotly==5.15.0
pip install matplotlib==3.7.1
pip install seaborn==0.12.2
pip install supabase==2.3.1
pip install fpdf2==2.7.4
pip install requests==2.31.0
pip install python-dotenv==1.0.0
pip install openpyxl==3.1.2
pip install xlsxwriter==3.1.2

echo.
echo ===============================================
echo    ¡INSTALACION COMPLETADA!
echo ===============================================
echo.
pause