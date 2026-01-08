# 📊 SheetGen – AI-Powered Excel Generator

SheetGen is a Python backend application that allows users to generate Excel files from natural language prompts using AI.

---

## 🚀 Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Docker

---

## environment variable

GROQ_API_KEY

## 📦 Getting Started
```
python -m venv venv
```

### Activite the enviroment
```
venv\Scripts\activate
```
### Install all

```
pip install -r requirements.txt
```
### Run app
```
uvicorn src.main:app --reload
```

## Run with docker
```
docker run -p 8000:8000 --env-file .env name
```