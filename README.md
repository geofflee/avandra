# Cheat Sheet

## Avandra

### Google Cloud CLI setup

```
winget install -e --id Google.CloudSDK

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

gcloud init

gcloud auth application-default login
```

### Create network

```
docker network create -d bridge scarlet
```

### Run local

```
python app/main.py --interactive --name=Hoglat --db=172.18.0.2
```

```
python app/main.py --interactive --name=Hoglat --db=172.18.0.2
```

```
docker run --network scarlet -it --rm -v $env:APPDATA\gcloud:/root/.config/gcloud geofflee/avandra
```

### Build

```
docker build -t geofflee/avandra .
```

### Push to DockerHub

```
docker push geofflee/avandra:latest
```

### Pull from DockerHub

```
sudo docker pull geofflee/avandra:latest
```

### Run cloud

```
sudo docker run --network scarlet -d --rm geofflee/avandra
```

## Postgres

### Init Postgres

```
docker run --network scarlet --name porygon -e POSTGRES_PASSWORD=changeme -d postgres:17-alpine
docker run --network scarlet -it --rm postgres:17-alpine psql -h porygon -U postgres -c 'CREATE DATABASE avandra;'
```

### Connect to Postgres

```
docker run --network scarlet -it --rm postgres:17-alpine psql -h porygon -U postgres -d avandra
```

## SSH

```
ssh -i rotom.key rotom@34.55.194.84
```
