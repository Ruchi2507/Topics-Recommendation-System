import pandas as pd
import gensim
import pickle

trainedModelFileName = 'trainedModels/word2vec_model.pickle'
knowledgeBaseFileName = 'trainedModels/knowledgeBase.pickle'

def readAndPreprocessDataSet():
    df = pd.read_csv("dataset/tag_sets.csv", header=None, delimiter=",")
    df.head()
    
    #Convert the dataFrame to list
    tagsList = df.values.tolist()
    #Delete the initial dataframe
    del df
    
    #Create list of list for the data read from tags_set
    #Inside list represents each row of csv file.
    tagsList = [str(tag[0]).split(',') for tag in tagsList]
    
    #TODO: Convert words to lowercase
    
    #Reading the user keywords as well
    df2 = pd.read_csv("dataset/user_keywords.tsv", delimiter='\t')
    keywordsList = df2["keywords"].values.tolist()
    keywordsList = [keywords.split(',') for keywords in keywordsList]
    del df2
    
    knowledgeBase = tagsList #+ keywordsList
    return knowledgeBase

def trainAndStoreWord2VecModel(knowledgeBase):    
    #Train Word2Vec model with the words in tag_set and user_keywords
    #For Word2Vec Training input format should be list of lists
    model = gensim.models.Word2Vec(knowledgeBase, min_count=1,size=300,workers=4)
    #save the trained model to disk
    with open(trainedModelFileName, "wb") as f:
        pickle.dump(model, f)

def createAndStoreFlattenedList(knowledgeBase):    
    #Flatten the knowledgeBase to get list of words/phrases in tag_set and user_keywords
    flatList = []
    for subList in knowledgeBase:
        for item in subList:
            flatList.append(item)
    knowledgeBase = flatList
    del flatList
    
    #Remove duplicacy from knowledgeBase to get list of unique words/phrases
    knowledgeBase = list(set(knowledgeBase))
    #save the flattened knowledgeBase (list of words/phrases) to disk
    #to be used for testing
    with open(knowledgeBaseFileName, "wb") as f:
        pickle.dump(knowledgeBase, f)

#for the given word find top 10 similar words from knowledgeBase
#if no similar word found in dictionary then empty JSON is returned.
def searchRelatedTopics(givenTopic=""):
    givenTopic = givenTopic.replace('+',' ')
    
    with open(trainedModelFileName, "rb") as f:
        model = pickle.load(f)
    
    with open(knowledgeBaseFileName, "rb") as f:
        knowledgeBase = pickle.load(f)
        
    relatedTopics={}
    topicSimilarityDict={}
    if givenTopic and givenTopic in model.wv.vocab:
        for topic in knowledgeBase:
            topicSimilarityDict[topic]= model.wv.similarity(givenTopic, topic)
    #Sort the topicSimilarityDict by values
    topicSimilarityDict = dict(sorted(topicSimilarityDict.items(), key=lambda item: item[1],reverse=True))
    #Get top 10 tags related to givenTopic
    relatedTopics["related_topics"] = [*topicSimilarityDict.keys()][:10]
    
    return relatedTopics

if __name__ == '__main__':
    print("Reading the Data Set")
    dataSet = readAndPreprocessDataSet()
    print("Training and Saving Word2Vec Model")
    trainAndStoreWord2VecModel(dataSet)    
    createAndStoreFlattenedList(dataSet)
    print("Test the saved Model")
    searchRelatedTopics("cat")