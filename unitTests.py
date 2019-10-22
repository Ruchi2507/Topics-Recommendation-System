"""
Unit testcases for Topic Recommender System
"""

from topicRecommenderSystem import readAndPreprocessDataSet
from topicRecommenderSystem import searchRelatedTopics

import unittest

def getActualTagsForTopic(givenTopic, knowledgeBase):
    """
    DESCRIPTION:
    ------------
    Searches for words/phrases which are related to 'givenTopic' and is present in given
    knowledgeBase.
    
    PARAMETERS:
    ------------
    1. givenTopic: given word/phrase for which related topics(i.e. words/phrases) need to be searched
    2. knowledgeBase: Dataset from which related words/phrases need to be searched
    """
    actualTagsList = []
    for tagsRow in knowledgeBase:
        for tag in tagsRow:
            if tag == givenTopic:
                actualTagsList.extend(tagsRow)
                break
    return actualTagsList

class testSearchedRelatedTopics(unittest.TestCase): 

    def setUp(self): 
        self.dataset = readAndPreprocessDataSet()
        pass
    
    def testRelatedTopicsForEmptyString(self):
        """
        DESCRIPTION:
        ------------
        For empty string predicted and actual tags should be empty list.
        """
        givenTopic = ""
        predictedTags = searchRelatedTopics(givenTopic)["related_topics"]
        assert len(predictedTags) == 0
        actualTags = getActualTagsForTopic(givenTopic, self.dataset)
        assert len(actualTags) == 0
        
    def testRelatedTopicsForUndefinedWord(self):
        """
        DESCRIPTION:
        ------------
        For undefined word predicted and actual tags should be empty list.
        """
        givenTopic = "wertyioh"
        predictedTags = searchRelatedTopics(givenTopic)["related_topics"]
        assert len(predictedTags) == 0
        actualTags = getActualTagsForTopic(givenTopic, self.dataset)
        assert len(actualTags) == 0
        
    def testRelatedTopicsForKeyword(self):
        """
        DESCRIPTION:
        ------------
        Returns True if predicted tags are subset of 
        tags specified in self.dataset for a given topic. 
        """
        givenTopic = "pokemon"
        predictedTags = searchRelatedTopics(givenTopic)["related_topics"]
        actualTags = getActualTagsForTopic(givenTopic, self.dataset)
        assert set(predictedTags).issubset(set(actualTags)) == True

    def testRelatedTopicsForPhrase(self):
        """
        DESCRIPTION:
        ------------
        Returns True if predicted tags are subset of 
        tags specified in self.dataset for a given phrase. 
        """
        givenTopic = "game of thrones"
        predictedTags = searchRelatedTopics(givenTopic)["related_topics"]
        actualTags = getActualTagsForTopic(givenTopic, self.dataset)
        assert set(predictedTags).issubset(set(actualTags)) == True

if __name__ == '__main__': 
    unittest.main()