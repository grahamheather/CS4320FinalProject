import urllib2
import json
from operator import itemgetter
from config import bot_id
from config import githubRepo
from config import waffle

def postOpenIssues():
    response = urllib2.urlopen("https://api.github.com/repos/"+githubRepo+"/issues")
    result = response.read()
    decoder = json.JSONDecoder()
    data = decoder.decode(result)
    string = '''The current issues are:\\n'''
    for issue in data:
            string += "* " + issue["title"] + "\\n"
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post", '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def postAllCards():
    response = urllib2.urlopen("https://api.waffle.io/"+waffle+"/cards/")
    result = response.read()
    decoder = json.JSONDecoder()
    data = decoder.decode(result)
    string = '''The cards are:\\n'''
    for card in data:
        string += "* " + card["githubMetadata"]["title"] + "\\n"
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def postProductBacklogCards():
    response = urllib2.urlopen("https://api.waffle.io/"+waffle+"/cards/")
    result = response.read()
    decoder = json.JSONDecoder()
    data = decoder.decode(result)
    string = '''The cards in the product backlog are:\\n'''
    for card in data:
        if card["githubMetadata"]["state"] == "open" and card["githubMetadata"]["labels"] == []:
            string += "* " + card["githubMetadata"]["title"] + "\\n"
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def postSprintBacklogCards():
    response = urllib2.urlopen("https://api.waffle.io/"+waffle+"/cards/")
    result = response.read()
    decoder = json.JSONDecoder()
    data = decoder.decode(result)
    string = '''The cards in the sprint backlog are:\\n'''
    for card in data:
        if card["githubMetadata"]["state"] == "open" and "help wanted" in map(itemgetter("name"), card["githubMetadata"]["labels"]):
            string += "* " + card["githubMetadata"]["title"] + "\\n"
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def postInProgressCards():
    response = urllib2.urlopen("https://api.waffle.io/"+waffle+"/cards/")
    result = response.read()
    decoder = json.JSONDecoder()
    data = decoder.decode(result)
    string = '''The cards in progress are:\\n'''
    for card in data:
        if card["githubMetadata"]["state"] == "open" and "in progress" in map(itemgetter("name"), card["githubMetadata"]["labels"]):
            string += "* " + card["githubMetadata"]["title"] + "\\n"
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

#def createStory():

#def assignPointsToStory():

def postSprintGoal():
    response = urllib2.urlopen("https://api.github.com/repos/"+githubRepo+"/milestones")
    result = response.read()
    decoder = json.JSONDecoder()
    data = decoder.decode(result)
    earliest = None
    earliest_milestone = None
    for milestone in data:
        if earliest == None:
            earliest = milestone['due_on']
            earliest_milestone = milestone
        # may want to check if the earliest sprint is actually unclosed but already completed sprint
        elif time.strptime(milestone['due_on'], "%Y-%m-%dT%H:%M:%SZ") < time.strptime(earliest, "%Y-%m-%dT%H:%M:%SZ"):
            earliest = milestone['due_on']
            earliest_milestone = milestone
    if earliest_milestone == None:
        string = "Cannot print current sprint goal: no current sprint"
    else:
        string = "The current sprint goal is:\\n" + milestone['description'].replace('\r', '').replace('\n', '\\n')
    print "https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}'
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')
            

#def postSprintLength():

#def postSprintStart():

#def postSprintEnd():

#def moveCard():

#def moveCardProductToSprintBacklog():

#def moveCardSprintBacklogToInProgress():

#def moveCardInProgressToComplete():

#def postDailyScrum():

#def setDailyScrumTime():

#def setSprintGoal():

#def setSprintStart():

#def setSprintEnd():

#def setSprintLength():

#def startSprintReview():

#def startSprintRetrospective():

postSprintGoal()
