"""
topicRecommenderSystem.py
It is responsible for finding the words/phrases related to initial query i.e. word/phrase
"""
import pandas as pd
import gensim
import pickle

#Trained model is saved as pickle file
trainedModelFileName = 'trainedModels/word2vec_model.pickle'

def readAndPreprocessDataSet():
    """
    DESCRIPTION:
    ------------
    This API is responsible for:
    - reading the dataset and converting the data to list of lists
      so that inner list represents a sentence consisting of words/phrases.
    - perform text pre-processing i.e. converting text to lowercase
    
    RETURN:
    -------
    Returns the list of list of tags where inner list represents different 
    tags (i.e. words/phrases) assigned by artist for an artwork and are
    considered are related.
    """
    df = pd.read_csv("dataset/tag_sets.csv", header=None, delimiter=",")
    df.head()
    
    #Convert the dataFrame to list
    tagsList = df.values.tolist()
    #Delete the initial dataframe
    del df
    
    #Create list of list for the data read from tags_set
    #Words are also converted to lowercase
    tagsList = [list(map(lambda x: x.lower(), str(tag[0]).split(','))) for tag in tagsList]
    
    return tagsList

def trainAndStoreWord2VecModel(knowledgeBase):    
    """
    DESCRIPTION:
    -----------
    Trains the Word2Vec model with the dataset received as argument.
    
    PARAMETERS:
    -----------
    knowledgeBase: list of lists. Inner list represents words/phrases related to an artwork.
    """
    #Train Word2Vec model with the words in tag_set 
    #For Word2Vec Training input format should be list of lists
    model = gensim.models.Word2Vec(knowledgeBase, min_count=1,size=300,workers=4,iter=5)
    #save the trained model to disk
    with open(trainedModelFileName, "wb") as f:
        pickle.dump(model, f)

def searchRelatedTopics(givenTopic=""):
    """
    DESCRIPTION:
    ------------
    - This API uses the trained model to predict the words/phrases which are
      related to given topic(i.e. word/phrase).
    - if no similar topic is found then empty dict is returned.
    
    PARAMETER:
    ----------
    Topic(i.e. word/phrase) for which related topics or tags(i.e words/phrases)
    need to be predicted.
    
    RETURN:
    ------
    Dict with key: related_topics and value as list of related topics
    """
    givenTopic = givenTopic.replace('+',' ')
    
    with open(trainedModelFileName, "rb") as f:
        model = pickle.load(f)
    
    relatedTopics={}
    relatedTopicsList=[]
    if givenTopic and givenTopic in model.wv.vocab:
        relatedTopicsList = list( map(lambda x: x[0],model.wv.most_similar(givenTopic)))    
    relatedTopics["related_topics"]=relatedTopicsList
    return relatedTopics

if __name__ == '__main__':
    """
    When this file is executed independently then:
    - it reads and pre-process the dataset i.e. tags assigned to different artwork
    - Train Word2Vec model and save the trained model as pickle file
    - Execute a sample test case
    """
    print("Reading the Data Set")
    dataSet = readAndPreprocessDataSet()
    print("Training and Saving Word2Vec Model")
    trainAndStoreWord2VecModel(dataSet)    
    print("Test the saved Model")
    print(searchRelatedTopics("cat"))