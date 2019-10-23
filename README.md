## Topics-Recommendation-System

### Objective
On th basis of initial query consisting of word/phrase, this system recommends topics or tags (i.e. words/phrases) which are related to give topic.

### Modules
1. topicRecommenderSystem.py: Responsible for training word2vec model and predicting the related topics/tags for given topic/tag.
2. unitTests.py: Unit tests for application which are created using Python unittest framework.
3. restAPI.py: REST APIs are created using Flask.

### Dataset
tag_sets.csv: Each row represents words or phrases related to an artwork.

### Dockerize and run the application
##### Build the container
- $ docker build -t rb-related-topics:latest .
- This step will install all the requirements, build the word2Vec model and execute unittests. 

##### Start the application
- $ docker run -d -p 8080:8080 rb-related-topics
- App is now up and listening to port 8080

##### Get recommendations
- Application listens to port 8080, and be queryable at http://localhost:8080/related_topics/<input>
- For example: 
  - GET: http://localhost:8080/related_topics/cats
  - Output: {
     "related_topics": [
       "kitty", 
       "kitten", 
       "cat", 
       "dogs", 
       "puppy", 
       "meow", 
       "doggi", 
       "dog", 
       "pug", 
       "puppies"
     ]
   }

### Running the application without docker
- Step 1: Build Word2Vec Model
  - Execute `python topicRecommenderSystem.py`
  - It trains and save word2vec model and defined APIs for predicting the similar topics
- Step 2: Run Unit tests
  - Execute `python unitTests.py` to automatically execute all the unit tests.
- Step 3: REST APIs
  - Execute `python restAPI.py`
  - Now app starts listening to port 8080 and recommended topics are queryable at http://localhost:8080/related_topics/<input>
  
NOTE: All these 3 steps are in Dockerfile as well.
