# Related Topics Search Rest API
from flask import Flask
from topicRecommenderSystem import searchRelatedTopics

app = Flask(__name__)

@app.route('/related_topics/<string:keyword>')
def getRelatedTopics(keyword):
    '''
    DESCRIPTION:
    ------------
    GET topics, which are related to given keyword or phrase.
    PARAMETERS:
    ----------
    1. keyword: given topic for which related topics need to be dumped.
    '''
    return searchRelatedTopics(keyword)

@app.route('/related_topics/')
def getEmptyTags():
    '''
    DESCRIPTION:
    ------------
    If no keyword is specified then empty list is returned
    '''
    return searchRelatedTopics("")

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8080)