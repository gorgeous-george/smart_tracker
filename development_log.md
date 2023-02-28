***
### 1. Planning
- analysis of the project purpose and architecture
- drafting apps (modules), data models, views, page templates

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
- create separate folder "tracker_core" that will contain a core django app
- go to created directory and activate virtual environment
```
source .venv/bin/activate
```
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
- open terminal on Ubuntu
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
It is useful to follow the post-installation steps (sudo privs, etc)
https://docs.docker.com/engine/install/linux-postinstall/

***
#### 2.3 Creation and configuring git repository
- create new repository at GitHub to have it as remote repository
- create and configure SSH keys
- configure branch protection rules for "main" branch at least
> https://github.com/gorgeous-george/smart_tracker
- initialize local git repository (if not done previously)
- set account's default identity (email and username)
```
$ git config --global user.email "you@example.com"
$ git config --global user.name "Your Name"
```
- create ".gitingore" file to keep a particular project directories/files unpublished
- add existed directories/files to git
- initial commit to local git repository
- renaming branch from "master" to "main"
- connect to remote GitHub new repository that has been created preliminary via GitHub.com website
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
- add appropriate commands and settings to the "core.Dockerfile"
- create ".core.env" file to keep secured the sensitive data required by docker-compose (DJANGO_SECRET_KEY, DB credentials, other variables)
- add ".core.env" file to ".gitignore"
- create and configure "docker-compose.yml" file (step-by-step: core service, db_core, and then others)
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
- in case a docker service is failed at OS level and/or
docker daemon is stopped and refused connections,
try to check the docker service's status first and then restart the service if needed
 ```
sudo service docker status
sudo service docker restart
```
***
#### 2.5 Configuring database layer (PostgreSQL for "core" service)
- install psycopg library within "core" virtual environment and update "requirements.txt" to have it in the image
```
pip install psycopg2-binary
pip freeze > requirements.txt
```
- update "core.settings.py" with DATABASES settings: set postgresql as db engine, set references to environment variables (db host, port, user, password, name)
- add appropriate environment variables to "core.env" file (host, port, user, password, name)
- add "db_core" service to "django-compose.yml" file
- create "docker-entrypoint.sh" and "wait-for-command.sh" to check that db is up before running services dependent on db
- update Dockerfile to run "docker-entrypoint.sh" and "wait-for-command.sh"
- re-build docker-compose
- in case of need, direct connect to "core" container's bash terminal (either via "exec" - existed instance or "run" - new instance). For example to run migrations and create superuser (need volumes to keep such changes), to check the logs, debug, etc.
```
sudo docker-compose exec core bash
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
exit
```
- in case of need, direct connect to the postgresql database
```
sudo docker-compose exec db_core psql --username=postgres --dbname=postgres
$ \l    # list databases
$ \du   # list roles
$ \?    # help
```
-in case of need, for development purposes, run manage.py with custom settings:
```
./manage.py COMMAND --settings=core.settings_local_sqlite_non-docker
```
***
#### 2.6 Installing and configuring django extensions and other tools:
- flake8
- widget-tweaks
### only for dev:
- django-debug-toolbar
- django-extensions
- ipython

***
#### 2.7 Configuring the microservices as docker containers
- tracker_core
- db_core

***
### 3. Development
*the app is designed to be run as docker container, however for development purposes additional settings are 
created as well. It makes possible to run the server using local sqlite.db without docker. 
The files of settings and db are added to ".gitignore". To run ./manage.py command with some specific 
"settings_dev.py", the following language is used:*
```
./manage.py <command> --settings=core.settings_dev
```

##### 3.1 Creating apps
- move to folder containing django "manage.py" file
- start a new app, add app_name to INSTALLED_APPS in "settings.py"
```
./manage.py startapp app_name
```
- 'auth_core' - custom authentication module
- 'dashboard' - core object's generic views, visualisation chart
- 'sandbox' - sandbox module (creation of custom objects' sets, namely groups of objects to track)
- 'tutorial' - quick instructions including SMART concept, dashboard and sandbox features
 
##### 3.2 Creating models
- 'dashboard':
  - created model representing a Dataset 
  - created model representing a Core Object
  - registering the models in "admin.py"

##### 3.3 Creating views
- 'auth_core': 
  - custom django generic class-based views (register, profile view, profile update)
- 'dashboard':
  - custom django generic class-based views (listview, detailview, CRUD pack) 
  
##### 3.4 Creating templates
- 'auth_core': 
  - pack of auth templates (login, logout, password, profile, register - TO ADD BOOTSTRAP FORMS,TO CHECK PASSWORD - TBD)
- 'dashboard':
  - base_generic
  - index
  - core object listview, detailview, form, and CRUD pack 
- 'dashboard': 
  - TBD
- 'sandbox':
  - TBD

##### 3.5 Creating forms
- 'auth_core':
  - UserCreationForm (django's pre-defined model form)
- 'dashboard':
  - CoreObjectForm (custom model form)

##### 3.6 Configuring urls
- ''
- index/
- admin/
- account/
  - django's pre-defined links to login, logout, password reset ('django.contrib.auth.urls')
  - custom links for register, view profile, update profile
- app/
  - core object list view, detail view, CRUD views
- dashboard/ TBD
- sandbox/ TBD

#### 3.7 Creating and configuring front-end files and scripts
- installed required scripts, namely added it to the base template:
  - Bootstrap
  - jQuery
  - CSS and JS scripts required by chosen Bootstrap design 
- created 'static/' folders to keep static files

***
### 4. Developing business logic and appropriate Celery tasks

***
### 5. Testing

***
### 6. Implementing (deploy)

***
### 7. Post-implementation checks
