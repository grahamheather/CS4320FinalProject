import urllib2
import json
import time
from datetime import datetime
from operator import itemgetter
from config import bot_id
from config import githubRepo
from config import waffle

# helper functions
def getCurrentMilestone():
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
    return earliest_milestone

# posting functions

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
    current_milestone = getCurrentMilestone()
    if current_milestone == None:
        string = "Cannot print current sprint goal: no current sprint"
    else:
        string = "The current sprint goal is:\\n" + current_milestone['description'].replace('\r', '').replace('\n', '\\n')
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def postSprintLength():
    current_milestone = getCurrentMilestone()
    if current_milestone == None:
        string = "Cannot print current sprint length: no current sprint"
    else:
        string = "The current sprint is " + str((datetime.strptime(current_milestone['due_on'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(current_milestone['created_at'], "%Y-%m-%dT%H:%M:%SZ")).days + 1) + " day(s) long."
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def postSprintStart():
    current_milestone = getCurrentMilestone()
    if current_milestone == None:
        string = "Cannot print current sprint start: no current sprint"
    else:
        string = "The current sprint began " + str((datetime.now() - datetime.strptime(current_milestone['created_at'], "%Y-%m-%dT%H:%M:%SZ")).days + 1) + " day(s) ago at " + current_milestone['created_at']
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def postSprintEnd():
    current_milestone = getCurrentMilestone()
    if current_milestone == None:
        string = "Cannot print current sprint end: no current sprint"
    else:
        string = "The current sprint ends in " + str((datetime.strptime(current_milestone['due_on'], "%Y-%m-%dT%H:%M:%SZ") - datetime.now()).days + 1) + " day(s) at " + current_milestone['due_on']
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

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
