# Etapa 1: Build - Instalar dependencias
FROM python:3.11-slim AS builder

# Instalar dependencias del sistema para compilar
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Crear un directorio para las dependencias de Python
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar e instalar requerimientos
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 2: Final - La imagen de producción
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el entorno virtual con las dependencias desde la etapa 'builder'
COPY --from=builder /opt/venv /opt/venv

# Copiar el código de la aplicación
COPY . .

# Activar el entorno virtual para los comandos siguientes
ENV PATH="/opt/venv/bin:$PATH"

# Exponer el puerto y ejecutar la aplicación
EXPOSE 8550
CMD ["python", "main.py"]
