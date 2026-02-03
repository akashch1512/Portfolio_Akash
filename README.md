# Portfolio

Minimal single-page portfolio built with Flask and a single HTML template.

**Local Run**
1. python -m venv .venv
1. .\.venv\Scripts\Activate.ps1
1. pip install -r requirements.txt
1. python app.py
1. Open http://localhost:8000

**Docker**
1. docker build -t portfolio .
1. docker run -p 8000:8000 portfolio

**Configuration**
- Update contact links and email in templates/index.html
- Set PORT to change the server port (default 8000)
- Set FLASK_DEBUG=1 for debug mode

**Structure**
- app.py (Flask entrypoint)
- templates/index.html (single-page UI)
