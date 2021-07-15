# COVID-19_Flask_Docker

The repository contains the docker files and the source files required to create images for COVID-19 models. To execute the models a flask app powered by gunicorn wsgi server running behind a nginx reverse proxy server is developed. 

# Build Instructions
Clone the Repo 
```
git clone https://github.com/aliasif1/COVID-19_Flask_Docker.git
```

# Build the flask gunicorn image
navigate to flask_gunicorn folder and run 

```
git image build -t <flask_gunicorn_img> .
```
<flask_gunicorn_img> can be any valid docker image name 

## Build the nginx reverse proxy image
navigate to nginx_proxy_server folder and run 

```
git image build -t <nginx_proxy_img> .
```
<nginx_proxy_img> can be any valid docker image name 

## Verify the build 
```
git image ls
```
The two images bild should pe part of the images list

#Use Prebuild Images 
The flask_gunicorn and nginx_proxy images are also available at docker hub.
```
docker image pull aliasifm/covid_flask_gunicorn:latest
```
```
docker image pull aliasifm/covid_ninx_proxy:latest
```

# Run the Services using docker compose 
## Initilaize swarm mode  
1. On one of the nodes (master node) run
```
docker swarm init 
```

2. Make other nodes join the swarm 
```
docker swarm join --token <token>
```

## Run the services 
1. Create swarm network 
```
docker network create web_network --driver overlay --subnet=192.168.100.0/24
```

2. Start the flask_gunicorn service 
```
docker service create --name webapp --replicas 4 --network web_network <flask_gunicorn_img>
```

3. start the nginx_proxy service
```
docker service create --name webproxy --network web_network -p 8080:80 <nginx_proxy_img>
```

## Verify that the services are up 
```
docker service ls
```

```
docker service ps webapp
```

```
docker service ps webproxy
```

# Test Out the App 
The application is a Flask Gunicorn app which is behind a nginx reverse proxy server. Docker does the load balancing for the incoming requests and redirects the request to flask containers

## Test the Api
Send a get request to
```
http://localhost:8080/home
```
You shuld get "Api is up" as repsone 

## Get Predictions from models
Send a post request to 
```
http://localhost:8080/predict
```

The Body of the post request should be a json list of inputs the covid model expects 
```
[{age: 8, sshx_data_abn_lung_asc: 0, sshx_data_altered_mental_state: 0, sshx_data_headache: 0, sshx_data_hypotension: 0, sshx_data_irritability_cnfsn: 0, sshx_data_loss_of_taste_smell: 0, sshx_data_malaise: 0, sshx_data_myalgia: 0, sshx_data_nasal_congestion: 0, sshx_data_nausea: 0, sshx_data_nose_bleed: 0, sshx_data_pain: 0, sshx_data_pharyngeal_exudate: 0, sshx_data_prostration: 0, sshx_data_rhinorrhea: 0, sshx_data_seizures: 0, sshx_data_difficulty_breathing: 0, sshx_data_sneezing: 0, sshx_data_sore_throat: 0, sshx_data_tachypnea: 0, sshx_data_vomiting: 0, sshx_data_other: 1, ch_mi: 0, ch_chf: 0, ch_pvd: 0, ch_cevd: 0, ch_dementia: 0, ch_cpd: 0, ch_rheumatic: 0, ch_pud: 0, ch_paraplegia: 0, ch_rd: 0, ch_cancer: 0, ch_mets: 0, diabetes: 0, liver: 0}]
```

The response would be a list where each item of the list corresponds to that input data set
