echo "Started pulling"
git pull

echo "Building Docker file!"
docker-compose up --build