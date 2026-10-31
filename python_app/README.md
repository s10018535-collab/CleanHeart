# CLEAN HEARTS - Python version

A Streamlit web app with a local SQLite database and sentence-transformers routing.

## Run it in VS Code

1. Open the `python_app` folder in VS Code.
2. Create and activate a virtual environment:
   - Windows: `python -m venv .venv` then `.venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
3. Install the requirements: `pip install -r requirements.txt`
4. Start the app: `streamlit run app.py`

The first start downloads the open source routing model (about 90 MB) once.
Reports are stored in `clean_hearts.db`, created automatically next to `app.py`.

## Officer portal

Choose a department, then enter the officer password. Officers only see reports routed to their department.
