@echo off
echo Starting Total Tech Serve website...
pip install -r requirements.txt -q
python generate_logo.py
python app.py
pause
