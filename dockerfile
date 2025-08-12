# Usa una imagen base de Python
FROM python:3.11-slim

# Instala dependencias del sistema necesarias para compilar paquetes si los hay
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia primero solo requirements.txt (mejor cacheo en builds)
COPY requirements.txt .

# Instala dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Luego copiamos el resto del proyecto
COPY . .

# Expone el puerto por defecto de Flet
EXPOSE 8550

# Comando para ejecutar la app
CMD ["python", "main.py"]
