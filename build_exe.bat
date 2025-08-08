@echo off
setlocal
IF NOT EXIST .venv (
  python -m venv .venv
)
call .venv\Scriptsctivate
pip install --upgrade pip
pip install -r requirements.txt pyinstaller
python assets\fetch_assets.py
pyinstaller --noconfirm --onefile --name "LoomianLegacyFanPlatformer" --add-data "assets;assets" main.py
echo Built to dist\LoomianLegacyFanPlatformer.exe
pause
