echo "Stopping docker containers"
docker stop celery_simple_worker

docker stop celery_flask_app

docker stop redis:4-alpine

echo "Started pulling"
git pull

echo "Building Docker file!"
docker-compose up --build