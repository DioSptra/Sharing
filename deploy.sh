#!/bin/bash
set -e

APP_DIR=/home/ubuntu/myapp   

GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
RESET="\033[0m"

echo -e "${BLUE}🚀 [1/4] Update & install dependencies...${RESET}"

echo -e "${RED}▶ MENJALANKAN : sudo apt-get update...${RESET}"
echo -e "${YELLOW}🔄 PLEASE WAIT . . . ${RESET}"
sudo apt-get update -y
echo -e "${GREEN}✅ UPDATE SELESAI ! ! ! ${RESET}\n"

echo -e "${RED}▶ MENGINSTALL DOCKER : sudo apt-get install -y docker.io...${RESET}"
echo -e "${YELLOW}🔄 PLEASE WAIT . . . ${RESET}"
sudo apt-get install -y docker.io docker-compose git
echo -e "${GREEN}✅ DOCKER SUDAH TERINSTALL ! ! ! ${RESET}"

echo -e "${BLUE}🔄 [2/4] Clone or pull latest code...${RESET}"

echo -e "${RED}▶ JIKA REPO SUDAH ADA MAKA RESET & PULL . . .${RESET}"
if [ -d "$APP_DIR" ]; then
echo -e "${YELLOW}🔄 CHECKING REPO AND UPDATE . . . ${RESET}"
  cd $APP_DIR
  git reset --hard
  git pull origin master
echo -e "${GREEN}✅ REPO SUDAH TERUPDATE ! ! !${RESET}\n"

echo -e "${RED}▶ JIKA REPO BELUM ADA MAKA CLONE UNTUK PERTAMA KALI . . .${RESET}"
else
echo -e "${YELLOW}🔄 JALANKAN PERINTAH : GIT CLONE . . . ${RESET}"
  git clone https://github.com/DioSptra/Sharing.git $APP_DIR
  cd $APP_DIR
fi
echo -e "${GREEN}✅ CLONE SELESAI ! ! !${RESET}\n"

echo -e "${BLUE}⚙️ [3/4] Build & start containers...${RESET}"

echo -e "${RED}▶ HENTIKAN CONTAINER LAMA . . .${RESET}"
echo -e "${YELLOW}🔄 PLEASE WAIT . . . ${RESET}"
sudo docker-compose down
echo -e "${GREEN}✅ CONTAINER LAMA DIHENTIKAN ! ! !${RESET}\n"

echo -e "${RED}▶ BUILD ULANG IMAGE . . .${RESET}"
echo -e "${YELLOW}🔄 PLEASE WAIT . . . ${RESET}"
sudo docker-compose build --no-cache
echo -e "${GREEN}✅ BUILD SELESAI ! ! !${RESET}\n"

echo -e "${RED}▶ MENJALANKAN CONTAINER BARU . . .${RESET}"
echo -e "${YELLOW}🔄 PLEASE WAIT . . . ${RESET}"
sudo docker-compose up -d
echo -e "${GREEN}✅ CONTAINER BERHASIL DIJALANKAN ! ! !${RESET}\n"

echo -e "${BLUE}🎉 [4/4] DEPLOYMENT COMPLETED ! ! !${RESET}"
sudo docker ps
