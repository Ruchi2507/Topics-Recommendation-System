FROM python:3.6

MAINTAINER Ruchika Chhabra "ruchika.chhabra25@gmail.com"

COPY . /app

WORKDIR /app

# Install the requirements
RUN pip install --default-timeout=400 -r requirements.txt

# Train word2Vec Model
RUN [ "python", "topicRecommenderSystem.py"]

# Run the UnitTests
RUN [ "python", "unitTests.py"]

EXPOSE 8080

# Command for REST API 
CMD [ "python", "./restAPI.py" ]