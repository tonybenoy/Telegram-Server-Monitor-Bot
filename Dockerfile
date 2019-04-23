# this is an official Python runtime, used as the parent image
FROM python:3.7.3-slim

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app
RUN apt-get update && apt-get install -y gcc
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# execute the Flask app
CMD ["python", "app.py"]
