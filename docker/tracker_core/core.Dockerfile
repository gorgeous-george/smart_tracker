# pull official base image
FROM python:3.10

# install dependencies
COPY ./tracker_core/requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# adding a layer to check DB availability before running the project
COPY ./docker/tracker_core/docker-entrypoint.sh ./docker/tracker_core/wait-for-command.sh /
RUN chmod +x /docker-entrypoint.sh /wait-for-command.sh

# copy project
COPY ./tracker_core/ /app

# set work directory
WORKDIR /app

# tells Docker that a container listens for traffic on the specified port
EXPOSE 8000

# set executables that will always run when the container is initiated
ENTRYPOINT ["/docker-entrypoint.sh"]

# set extra default arguments that could be overwritten from the command line when the docker container runs
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]