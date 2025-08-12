activar el ambiente:
source /home/cbordaberry/Documentos/Python/prueba_front/venv/bin/activate

para ejecutar la app:
python main.py

para construir la imagen:
docker build -t caidas-web .

para construir el contenedor:
docker run -p 8550:8550 caidas-web



para enviar la imagen al .53:
cd /home/cbordaberry/Documentos/Python/images_hub/


guardar las imagenes generadas como archivos:
docker save -o caidas-web.tar caidas-web:latest
docker save -o caidas-api.tar caidas-api:latest


enviar esos archivos al .53:
scp caidas-web.tar caidas-api.tar asosa@10.5.2.53:/home/cbordaberry/docker_hub


en el .53:
docker load -i caidas-web.tar
docker load -i caidas-api.tar


y construir los contenedores en el .53:
docker images
docker run -d -p 8550:8550 caidas-web
docker run -d -p 8103:8000 --hostname caidas-api --name caidas-api caidas-api