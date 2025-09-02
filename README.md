# Proyecto Flet - App de Caídas

## Desarrollo Local

### 1. Activar el entorno virtual

Para trabajar en el proyecto, primero activa el entorno virtual de Python.

```bash
source venv/bin/activate
```

### 2. Ejecutar la aplicación

Una vez activado el entorno, puedes ejecutar la aplicación localmente.

```bash
python main.py
```

---

## Despliegue con Docker

Sigue estos pasos para empaquetar la aplicación en una imagen de Docker, transferirla a un servidor y ejecutarla.

### Prerrequisitos

*   Docker instalado localmente y en el servidor.
*   Acceso SSH al servidor.

### 1. Construir la imagen de Docker

En la raíz del proyecto, ejecuta el siguiente comando para construir la imagen. Puedes cambiar `caidas-web:latest` por el nombre y tag que prefieras.

```bash
docker build -t caidas-web:latest .
```

### 2. Guardar la imagen en un archivo .tar

Exporta la imagen creada a un archivo `.tar` para poder transferirla fácilmente.

```bash
docker save -o caidas-web.tar caidas-web:latest
```

### 3. Transferir la imagen al servidor

Usa `scp` para copiar el archivo `.tar` a tu servidor. Reemplaza `usuario`, `ip-del-servidor` y la ruta de destino según corresponda.

```bash
scp caidas-web.tar usuario@ip-del-servidor:/ruta/en/el/servidor/
```
*Ejemplo real que usaste:*
`scp caidas-web.tar asosa@10.5.2.53:/home/cbordaberry/images_import/`


### 4. Cargar la imagen en el servidor

Primero, conéctate a tu servidor vía SSH.

```bash
ssh usuario@ip-del-servidor
```

Una vez en el servidor, navega al directorio donde subiste el archivo y carga la imagen de Docker desde el archivo `.tar`.

```bash
docker load -i caidas-web.tar
```

### 5. Ejecutar el contenedor

Finalmente, ejecuta el contenedor desde la imagen cargada. Esto expondrá la aplicación en el puerto `8550` del servidor.

```bash
docker run -d --rm -p 8550:8550 --name caidas-web-container api-merienda:latest
```

**Explicación de los parámetros de `docker run`:**
-   `-d`: Ejecuta el contenedor en segundo plano (detached mode).
-   `--rm`: Elimina automáticamente el contenedor cuando se detiene.
-   `-p 8550:8550`: Mapea el puerto 8550 del host al puerto 8550 del contenedor.
-   `--name caidas-web-container`: Asigna un nombre al contenedor para identificarlo fácilmente.
