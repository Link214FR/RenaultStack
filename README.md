# RenaultStack

## Requirements : 
- git : sudo apt install git (to retrieve project file)
- docker : sudo apt install docker
- docker-compose : sudo apt install docker-compose

# Getting started

- mkdir ev-dashboard
- cd ev-dashboard
- git clone https://github.com/Link214FR/RenaultStack

## Edit cofnig files : 

- mv ev-dashboard/myev/app/vehicleCredentials.json.example ev-dashboard/myev/app/vehicleCredentials.json
- nano ev-dashboard/myev/app/vehicleCredentials.json => Configure your Renault credentials
- mv dashboard/prometheus/prometheus.yml.example dashboard/prometheus/prometheus.yml
- nano dashboard/prometheus/prometheus.yml.example => line 50 replace VF1XXXXXXXXXXXXXX by your VIN

## prepare docker ressources

- ddocker network create monitor

## start server

- cd ev-dashboard
- sudo docker compose up -d
- cd ../dashboard
- sudo docker compose up -d
 
grafana should be available on your computer at port 3000 with default credentials

# Optional : configure NPM to access all backend and more secure stuff

... TODO
  
