***
### 1. Planning
- analysis of the project purpose and architecture
- drafting models, views, page templates

***
### 2. Creation of project environment

- install Python
- install Git
- install PyCharm
- create root project folder
- create "README.md", "development_log.md"	
- init empty local git repository

***
#### 2.1 Installing Django

- create separate folder that will contain django app particularly
- activate virtual environment
- update pip for future use
- install Django framework and initial libraries, creating "requirements.txt"
- start django project named "core"
- secure SECRET_KEY via environment variable
- test run
```
$ django-admin startproject core .
$ python manage.py runserver
```

***
#### 2.2 Installing Docker

- open the terminal on Ubuntu
- remove any Docker files that are running in the system
- check if the system is up-to-date
- install Docker
- install all the dependency packages
- before testing Docker, check the version installed
- pull an image from the Docker hub
- check if the docker image has been pulled and is present in your system
- display all the containers pulled
- check for containers in a running state

```
$ sudo apt-get remove docker docker-engine docker.io
$ sudo apt-get update
$ sudo apt install docker.io
$ sudo snap install docker
$ docker --version
$ sudo docker run hello-world
$ sudo docker images
$ sudo docker ps -a
$ sudo docker ps
```

That's it, Docker is successfully installed on Ubuntu!
It is useful to follow the post-installation steps
https://docs.docker.com/engine/install/linux-postinstall/

***
#### 2.3 Creation and configuring git repository

- create new repository at GitHub to have it as remote repository
- create and configure SSH keys
- configure branch protection rules for "main" branch at least
> https://github.com/gorgeous-george/smart_tracker
- initialize local git repository
- set account's default identity (email and username)
```
$ git config --global user.email "you@example.com"
$ git config --global user.name "Your Name"
```
- create ".gitingore" file to keep a particular project directories/files unpublished
- add existed directories/files to git
- initial commit to local git repository
- renaming branch from "master" to "main"
- connect to remote GitHub new repository that has been created preliminary via github.com website
- push the init commit to remote repository
- create local branch "develop" && switch to it && add files to git tracker
```
cd && cd PycharmProjects/dummy_shop
git init
touch README.md
touch .gitignore
git add .
git commit -m "initial commit"
git branch -m main
git remote add origin git@github.com:gorgeous-george/dummy_shop.git
git push -u origin main
git branch develop && git checkout develop && git add .
```

That's it, local Git repository has been created and connected to remote GitHub repository.

**Code committing and pushing workflow is supposed to be the following:**
- Code development is performed within separate local branch "develop". Local commits are created and then pushed to GitHub branch "develop"
```
git branch develop && git checkout develop
git add .
git status
git commit -m 'commit message'
git push --set-upstream origin develop
```
- At GitHub a pull request is created to merge branch "develop" to branch "main"
- GitHub branch "develop" is deleted
- Local branch "main" is synchronized with GitHub branch "main"
- Local branch "develop" is deleted
```
git checkout main && git pull
git branch --delete develop
```
- Back to the first step

***
#### 2.4 Containerization - configuring docker and docker-compose

- create folder "docker" to have all settings there
- create folder "core" for the Django application that will be run as microservice within Docker
- create Dockerfile "core.Dockerfile"
- add appropriate commands and settings to the Dockerfile
- create "core.env" file to keep secured the sensitive data required by docker-compose (DJANGO_SECRET_KEY and DB credentials)
- add "core.env" file to ".gitignore"
- create and configure "docker-compose.yml" file
- build and run up the docker-compose
```
sudo docker-compose build
sudo docker-compose up
...
CTRL+C
sudo docker-compose down
```
- to delete all images, volumes and containers (in case of need)
```
sudo docker system prune -a --volumes
```
- to delete unhealthy container
```
sudo systemctl restart docker.socket docker.service
```
- to kill all the processes associated with port 8000
```
sudo fuser -k 8000/tcp
```
***
#### 2.5 Configuring database layer (PostgreSQL for "core" service)

- install psycopg library within "core" virtual environment and update "requirements.txt" to have it in the image
```
pip install psycopg2-binary
pip freeze > requirements.txt
```
- update "core.settings.py" with DATABASES settings: engine for postgresql, and host, port, user, password, name as references to environment variables (for security purposes)
- add appropriate environment variables to "core.env" file (host, port, user, password, name)
- add "db_core" service to "django-compose.yml" file
- create "docker-entrypoint.sh" and "wait-for-command.sh" to check that db is up before running services dependent on db
- update Dockerfile to run "docker-entrypoint.sh" and "wait-for-command.sh"
- re-build docker-compose
- connect to "core" container's bash terminal to run migrations and create superuser (it lives only at the container level)
```
sudo docker-compose exec core bash
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
exit
```
- in case of need connect to the database
```
sudo docker-compose exec db_core psql --username=postgres --dbname=postgres
$ \l    # list databases
$ \du   # list roles
$ \?    # help
```

***
#### 2.6 Configuring django extensions and tools:

***
#### 2.7 Configuring the microservices as docker containers

***
### 3. Development

#### 3.1 "{app_name}" service
##### Creating apps
##### Creating models
##### Creating views
##### Creating templates
##### Creating forms
##### Configuring urls

***
### 4. Developing business logic and appropriate Celery tasks

***
### 5. Testing

***
### 6. Implementing (deploy)

***
### 7. Post-implementation checks
