#!/bin/bash
set -e

APP_DIR=/home/ubuntu/myapp   

echo "[1/4] Update & install dependencies..."
sudo apt-get update -y
sudo apt-get install -y docker.io docker-compose git

echo "[2/4] Clone or pull latest code..."
if [ -d "$APP_DIR" ]; then
  cd $APP_DIR
  git reset --hard
  git pull origin master
else
  git clone https://github.com/DioSptra/Sharing.git $APP_DIR
  cd $APP_DIR
fi

echo "[3/4] Build & start containers..."
sudo docker-compose down
sudo docker-compose build --no-cache
sudo docker-compose up -d

echo "[4/4] Deployment finished!"
sudo docker ps
