# Imagen base de Python (ligera)
FROM python:3.13-slim

# Evita archivos .pyc y buffer en logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos requirements primero (mejor cache)
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Comando para correr la app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
