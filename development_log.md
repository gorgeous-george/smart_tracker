***
### 1. Planning
<details>

- analysis of the project purpose and architecture
- drafting apps (modules), data models, views, page templates
- designing business logic

</details>

***
### 2. Creation of project environment
<details>

- install Python
- install Git
- install PyCharm
- create root project folder
- create "README.md", "development_log.md"	
- init empty local git repository

***
#### 2.1 Installing Django
<details>

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

</details>

***
#### 2.2 Installing Docker
<details>

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

</details>

***
#### 2.3 Configuring git repository
<details>

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

</details>

***
#### 2.4 Containerization - configuring docker and docker-compose
<details>

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
  
</details>

***
#### 2.5 Configuring database layer (PostgreSQL for "core" service)
<details>

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

</details>

***
#### 2.6 Installing and configuring django extensions and other tools:
<details>

- flake8
- widget-tweaks
only for dev:
- django-debug-toolbar
- django-extensions
- ipython

</details>

***
#### 2.7 Configuring the microservices as docker containers
<details>

- core:
  - build image from the 'tracker_core' django project (it also includes DRF),
  - added ports, networks, volumes, dependencies,
  - added env. file.
- db_core:
  - pull postgresql image from dockerhub, 
  - added ports, networks, volumes,
  - added DB credentials to env. file (HOST, NAME, USER, PASS),
  - added DB settings and credentials to django settings.py.
- pgadmin:
  - pull pgadmin image from dockerhub.
- redis:
  - pull image from docker-hub,
  - added ports, networks, volumes,
  - added appropriate data to "settings.py" to use redis as celery broker and cache,
  - added redis and django-redis to requirements.txt.
- celery:
  - added celery and "celery[redis]" to requirements.txt,
  - added 'celery.py' to django core folder, 
  - updated '__init__.py' in django core folder,
  - added broker_url and result_backend to django 'settings.py',
  - created 'tasks.py' in django 'dashboard' app,
  - build image based on the 'tracker_core' django project.
- flower:
  - pull image from dockerhub,
  - specified environment variables,
  - specified command to run flower.
- mailhog
  - pull image from dockerhub,
  - added email backend, host, port, user, password to settings.py.

- networks
- volumes

</details>

</details>

***
### 3. Development of django application
<details>

*the app is designed to be run as docker container, however for development purposes additional settings are 
created as well. It makes possible to run the server using local sqlite.db without docker. 
The files of settings and db are added to ".gitignore". In case of need, for development purposes run ./manage.py 
command with custom settings:*
```
./manage.py runserver --settings=core.settings_local_sqlite_non-docker
./manage.py makemigrations --settings=core.settings_local_sqlite_non-docker
etc
```
##### 3.1 Creating apps
<details>

- move to folder containing django "manage.py" file
- start a new app, add app_name to INSTALLED_APPS in "settings.py"
```
./manage.py startapp app_name
```
- 'auth_core' - custom authentication module
- 'dashboard' - core object's generic views, visualisation chart
- 'sandbox' - sandbox module (creation of custom objects' sets, namely groups of objects to track)
- 'tutorial' - quick instructions including SMART concept, dashboard and sandbox features

</details>

##### 3.2 Creating models
<details>

- 'dashboard':
  - created model representing a Dataset 
  - created model representing a Core Object
  - registering the models in "admin.py"

</details>

##### 3.3 Creating views
<details>

- 'auth_core': 
  - custom django generic class-based views (register, profile view, profile update)
- 'dashboard':
  - custom django functional views (dashboard table, chart, filter, buttons) 
- 'sandbox':
  - custom django functional views (dataset table, object table, related CRUD functions, buttons and filters)
- 'tutorial':
  - simple index view

</details>

##### 3.4 Creating templates
<details>

- 'auth_core': 
  - pack of auth templates (login, logout, password, profile, register - TO ADD BOOTSTRAP FORMS,TO CHECK PASSWORD - TBD)
- 'dashboard':
  - base_generic template (navbar, sidebar)
  - index (home page)
  - dashboard page with includes (forms, object list, chart + CSS/JS)
- 'sandbox': 
  - sandbox page with includes (CRUD, form, list - for dataset and object appropriately + CSS/JS)
- 'tutorial':
  - tutorial page

</details>

##### 3.5 Creating forms
<details>

- 'auth_core':
  - UserCreationForm (django's pre-defined model form)
- 'dashboard':
  - DashboardFilterForm (custom django form). This form uses Dataset queryset so that special try-except logic
  is designed to avoid errors during the very first start before migrations applied so that queryset is not available.
- 'sandbox':
  - DatasetModelForm (pure django model form)
  - DatasetObjectModelForm (pure django model form)

</details>

##### 3.6 Configuring urls
<details>

- 'core': index, admin, API
- 'auth_core': django's pre-defined links to login, logout, password reset ('django.contrib.auth.urls'), 
custom links for register, view profile, update profile
- 'dashboard': base dashboard page and 'filtered/' for filter results
- 'sandbox': base sandbox page, CRUD for dataset and object appropriately, dataset filters
- 'tutorial': tutorial page

</details>

#### 3.7 Configuring static files and scripts
<details>

- created 'static/' folders to keep static files for the whole project and for each app appropriately
- added CSS/JS to the 
  - base generic template: MDBootstrap, jQuery, Popper, Feather icons + feather.replace() command, 
  Google Chart loader, custom JS for Messages timeout.
  - dashboard template: Google Chart JS, custom CSS, custom Ajax scripts 
  - sandbox template: custom Ajax scripts, feather.replace() command

</details>

#### 3.8 Configuring Django REST Framework application as a separate module of main Django application

<details>

- installed required packages into project's virtual environment.
```
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
```
- created custom DRF application.
```
./manage.py startapp rest_framework_app --settings=core.settings_local_sqlite_non-docker
```
- configured 'settings.py'
```
INSTALLED_APPS = [
    ...
    'rest_framework_app',
]
REST_FRAMEWORK = {
    # Pagination settings
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
}
```
- created 'serializers.py': added serializers for User, Dataset and CoreObject models.
- 'views.py': added ViewSets using User, Dataset and CoreObject serializer. 
- 'core.urls.py': added 'include' referring to rest_framework_app.urls.
- 'urls.py': added urlpatterns, registered routes for User, Dataset and CoreObject ViewSets.

</details>

</details>

***
### 4. Developing business logic
<details>
 
- SMART concept is hard-coded to COREOBJECT model, so that each object has appropriate settings (current value, 
priority, measure, time frame, responsible).
- Each object would have one of three statuses based on simple pattern "Red-Orange-Green". Each object has its own 
level of priority and current value set by user, so that after object creation/update the application sets status of 
the object comparing current value with the priority. It is hard-coded by functional view at SANDBOX. 
- SANDBOX page has custom filters (SEE OBJECTS, SHOW ALL OBJECTS). It is designed as jQuery/Ajax + JS + custom 
functional views.
- SANDBOX page has buttons to Create, Edit and Delete datasets and objects. It is designed appropriately as modals +
ModelForms + jQuery/Ajax + JS + custom functional views returning JSON + HTML includes.
- SANDBOX page has buttons to Delete all data and to create Starter pack of datasets/objects.
- DASHBOARD page has custom filters. It is designed as custom django form + jQuery/Ajax + JS + custom functional views 
returning JSON + HTML includes.
- DASHBOARD has Pie Chart that is re-drawn appropriately to filter applied. It is designed as jQuery/Ajax + JS + custom 
functional views returning JSON + HTML includes

</details>

***
### 5. Testing
<details>
TBD
</details>

***
### 6. Implementing (deploy)
<details>
TBD
</details>

***
### 7. Post-implementation checks
<details>
TBD
</details>
