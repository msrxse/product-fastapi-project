# **Project Startup**

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install all deps using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. Start uvicorn server - reload already integrated

   ```bash
   fastapi dev app/main.py
   ```
