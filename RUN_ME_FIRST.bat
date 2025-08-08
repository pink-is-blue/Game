@echo off
setlocal
IF NOT EXIST .venv (
  python -m venv .venv
)
call .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

REM Auto-download assets then run the game
python assets\fetch_assets.py
python main.py
