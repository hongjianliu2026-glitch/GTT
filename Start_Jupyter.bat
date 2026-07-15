@echo off
cd /d C:\GTT

echo Starting Jupyter...
echo Please keep this window open.
echo.

start "" "http://127.0.0.1:8899/lab"

python -m jupyter lab --no-browser --port=8899 --ServerApp.token="" --ServerApp.password=""

echo.
echo Jupyter stopped or failed.
pause