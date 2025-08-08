#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv || true
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt pyinstaller
python assets/fetch_assets.py
pyinstaller --noconfirm --onefile --name "LoomianLegacyFanPlatformer" --add-data "assets:assets" main.py
echo Built to dist/LoomianLegacyFanPlatformer
