
#!/bin/bash
chmod +x start.sh
pip install --upgrade pip
pip install -r requirements.txt
exec uvicorn main:app --host=0.0.0.0 --port=$PORT
    
