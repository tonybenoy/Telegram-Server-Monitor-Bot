# this is an official Python runtime, used as the parent image
FROM python:3.9.13-slim

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app
RUN apt-get update && apt-get install -y gcc libffi-dev
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get remove -y gcc libffi-dev
# execute the app
CMD ["python", "app.py"]
