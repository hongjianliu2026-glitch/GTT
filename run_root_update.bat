@echo off
cd /d C:\GTT
python build_RootAddon.py
copy /Y C:\GTT\EnglishDB\CSV\RootDB_PLUS.csv C:\GTT\EnglishDB\CSV\RootDB.csv
python build_GTT_RootDB.py
pause