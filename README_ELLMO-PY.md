# Prepare
- create / activate  .venv (python 12)
- install requiremetns
- ollmaa must be installed an running
```
python3 --version
python3 -m venv .venv

python source .venv/bin/activate
pip install -r requirements.txt  
```


# ./chat
Python OLLAMA terminal chat demo.
```bash
cd chat
python chat.py
```

# ./vision
Python OLLAMA  LLAVA terminal demo - capture and interpret image.
```bash
cd vision
python vision.py
```

# ./backend 
FastAPI demo with OLLAMA endpoints.
```bash
cd backend
uvicorn main:app --reload
```
Server will be available at http://127.0.0.1:8000
See http://127.0.0.1:8000/docs