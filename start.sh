
#!/bin/bash
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT
    
