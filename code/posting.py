import urllib2
import json
import time
from datetime import datetime, timedelta
from operator import itemgetter
from config import bot_id
from config import githubRepo
from config import waffle
from config import githubOAuth
from config import dailyScrumTime

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


# create and modify stories

def createStory(story_name):
    response = urllib2.urlopen("https://api.github.com/repos/"+githubRepo+"/issues?access_token=" + githubOAuth, data='{"title": "' + story_name + '"}')
    result = response.read()
    decoder = json.JSONDecoder()
    data = decoder.decode(result)
    string = "Story '" + story_name + "' created."
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post", '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

#def assignPointsToStory():

def moveCardProductToSprintBacklog(story_name):
    response = urllib2.urlopen("https://api.github.com/repos/"+githubRepo+"/issues")
    result = response.read()
    decoder = json.JSONDecoder()
    data = decoder.decode(result)
    requested_story = None
    found = False
    for card in data:
        if card["title"].lower() == story_name:
            found = True
            requested_story = card
    if not found:
        string = "Could not move the story from the product backlog to the sprint backlog: story not found"
    elif requested_story["state"] == "open" and "in progress" not in map(itemgetter("name"), requested_story["labels"]) and "help wanted" not in map(itemgetter("name"), requested_story["labels"]):
        string = "Story '" + story_name + "' moved from the product backlog to the sprint backlog"
        response = urllib2.urlopen("https://api.github.com/repos/"+githubRepo+"/issues/" + str(requested_story["number"]) + "/labels?access_token=" + githubOAuth, data='["help wanted"]')
        result = response.read()
        decoder = json.JSONDecoder()
        data = decoder.decode(result)
    else:
        string = "Could not move the story from the product backlog to the sprint backlog: story not in product backlog"
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post", '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def moveCardSprintBacklogToInProgress(story_name):
    response = urllib2.urlopen("https://api.github.com/repos/"+githubRepo+"/issues")
    result = response.read()
    decoder = json.JSONDecoder()
    data = decoder.decode(result)
    requested_story = None
    found = False
    for card in data:
        if card["title"].lower() == story_name:
            found = True
            requested_story = card
    if not found:
        string = "Could not move the story from the sprint backlog to in progress: story not found"
    elif requested_story["state"] == "open" and "help wanted" in map(itemgetter("name"), requested_story["labels"]):
        string = "Story '" + story_name + "' moved from the sprint backlog to in progress"
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request('https://api.github.com/repos/'+githubRepo+"/issues/" + str(requested_story["number"]) + "/labels/help%20wanted?access_token=" + githubOAuth)
        request.get_method = lambda: 'DELETE'
        response = opener.open(request)
        response = urllib2.urlopen("https://api.github.com/repos/"+githubRepo+"/issues/" + str(requested_story["number"]) + "/labels?access_token=" + githubOAuth, data='["in progress"]')
        result = response.read()
        decoder = json.JSONDecoder()
        data = decoder.decode(result)
    else:
        string = "Could not move the story from the sprint backlog to in progress: story not in sprint backlog"
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post", '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}') 

def moveCardInProgressToDone(story_name):
    response = urllib2.urlopen("https://api.github.com/repos/"+githubRepo+"/issues")
    result = response.read()
    decoder = json.JSONDecoder()
    data = decoder.decode(result)
    requested_story = None
    found = False
    for card in data:
        if card["title"].lower() == story_name:
            found = True
            requested_story = card
    if not found:
        string = "Could not move the story from in progress to done: story not found"
    elif requested_story["state"] == "open" and "in progress" in map(itemgetter("name"), requested_story["labels"]):
        string = "Story '" + story_name + "' moved from in progress to done"
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request('https://api.github.com/repos/'+githubRepo+"/issues/" + str(requested_story["number"]) + "/labels/in%20progress?access_token=" + githubOAuth)
        request.get_method = lambda: 'DELETE'
        response = opener.open(request)
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request('https://api.github.com/repos/'+githubRepo+"/issues/" + str(requested_story["number"]) + "?access_token=" + githubOAuth, data='{"state": "closed"}')
        request.get_method = lambda: 'PATCH'
        response = opener.open(request)
    else:
        string = "Could not move the story from in progress to done: story not in progress"
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post", '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

# set sprint properties

def setDailyScrumTime(timeString):
    # NOT persistent
    dailyScrumTime = time.strptime(timeString, "%H:%M")
    string = "Daily Scrum meeting time updated to " + timeString
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post", '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def setSprintGoal(new_description):
    current_milestone = getCurrentMilestone()
    if current_milestone == None:
        string = "Cannot set current sprint goal: no current sprint"
    else:
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request('https://api.github.com/repos/'+githubRepo+"/milestones/" + str(current_milestone["number"]) + "?access_token=" + githubOAuth, data='{"description": "' + new_description + '"}')
        request.get_method = lambda: 'PATCH'
        response = opener.open(request)
        string = "The current sprint goal has been updated to:\\n" + new_description
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def setSprintEnd(dateString):
    current_milestone = getCurrentMilestone()
    if current_milestone == None:
        string = "Cannot update current sprint end: no current sprint"
    else:
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        # unsure why it is necessary to add the extra day
        request = urllib2.Request('https://api.github.com/repos/'+githubRepo+"/milestones/" + str(current_milestone["number"]) + "?access_token=" + githubOAuth,
                                  data='{"due_on": "' + datetime.strftime(datetime.strptime(dateString, "%m/%d/%Y") + timedelta(days=1), "%Y-%m-%dT%H:%M:%SZ") + '"}')
        request.get_method = lambda: 'PATCH'
        response = opener.open(request)
        string = "The current sprint now ends in " + str((datetime.strptime(dateString, "%m/%d/%Y") - datetime.now()).days + 1) + " day(s) on " + dateString
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')


# sprint meetings

def startSprintPlanning():
    string = "Beginning sprint planning meeting now."
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')
    current_milestone = getCurrentMilestone()
    if current_milestone == None:
        string = "Cannot estimate recommended sprint planning meeting length: current sprint length not found"
    else:
        meeting_length = ((datetime.strptime(current_milestone['due_on'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(current_milestone['created_at'], "%Y-%m-%dT%H:%M:%SZ")).days + 1) * 2 / 7
        string = "It is recommended that the sprint planning meeting last less than " + str(meeting_length) + " hours as there are " + str((datetime.strptime(current_milestone['due_on'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(current_milestone['created_at'], "%Y-%m-%dT%H:%M:%SZ")).days + 1) + " days in this sprint.  It should end by " + datetime.strftime((datetime.now() + timedelta(hours=meeting_length)), "%H:%M")
        response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')
    postProductBacklogCards()
    time.sleep(60*60*meeting_length)
    string = "Sprint planning meeting time limit expired."
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def startDailyScrum():
    dayStart = datetime.now() - timedelta(days=1)
    dayEnd = datetime.now()
    current_milestone = getCurrentMilestone()
    info = {}
    if not current_milestone == None:
        response = urllib2.urlopen("https://api.waffle.io/"+waffle+"/cards/")
        result = response.read()
        decoder = json.JSONDecoder()
        data = decoder.decode(result)
        for card in data:
            cardFinished = datetime.strptime(card["githubMetadata"]["closed_at"], "%Y-%m-%dT%H:%M:%S.000Z") 
            if card["githubMetadata"]["state"] == "closed" and cardFinished > dayStart and cardFinished < dayEnd:
                if "assignees" in card["githubMetadata"] and card["githubMetadata"]["assignees"] != []:
                    for assignee in card["githubMetadata"]["assignees"]:
                        if assignee["login"] not in info.keys():
                            info[assignee["login"]] = {"did":[], "willDo":[], "impediments":[]}
                        info[assignee["login"]]["did"] += [card["githubMetadata"]["title"]]
            elif card["githubMetadata"]["state"] == "open" and "in progress" in map(itemgetter("name"), card["githubMetadata"]["labels"]):
                if "assignees" in card["githubMetadata"] and card["githubMetadata"]["assignees"] != []:
                    for assignee in card["githubMetadata"]["assignees"]:
                        if assignee["login"] not in info:
                            info[assignee["login"]] = {"did":[], "willDo":[], "impediments":[]}
                        info[assignee["login"]]["willDo"] += [card["githubMetadata"]["title"]]

        response = urllib2.urlopen("https://api.github.com/repos/"+githubRepo+"/issues")
        result = response.read()
        decoder = json.JSONDecoder()
        data = decoder.decode(result)
        requested_story = None
        for card in data:
            cardCreated = datetime.strptime(card["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if card["state"] == "open" and cardCreated > dayStart and cardCreated < dayEnd:
                if card["user"]["login"] not in info:
                    info[card["user"]["login"]] = {"did": [], "willDo": [], "impediments" :[]}
                info[card["user"]["login"]]["impediments"] +=[card["title"]]

        string = "Daily Scrum:\\n"
        for person in info:
            string += "\\n" + person + ":\\n\\tDid:\\n"
            for story in info[person]["did"]:
                string += "\\t\\t* " + story + "\\n"
            string += "\\tWill do today:\\n"
            for story in info[person]["willDo"]:
                string += "\\t\\t* " + story + "\\n"
            string += "\\tImpediments:\\n"
            for story in info[person]["impediments"]:
                string += "\\t\\t* " + story + "\\n"
    else:
        string = "Could not post daily scrum meeting: current sprint not found"
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def startSprintReview():
    string = "Beginning sprint review meeting now."
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')
    current_milestone = getCurrentMilestone()
    if current_milestone == None:
        string = "Cannot estimate recommended sprint review meeting length: current sprint length not found"
    else:
        sprintStart = datetime.strptime(current_milestone['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        sprintEnd = datetime.strptime(current_milestone['due_on'], "%Y-%m-%dT%H:%M:%SZ")
        meeting_length = ((sprintEnd - sprintStart).days + 1) * 2 / 7
        string = "It is recommended that the sprint review meeting last less than " + str(meeting_length) + " hours as there were " + str((sprintEnd - sprintStart).days + 1) + " days in this sprint (using the 2 hours / week of sprint rule).  It should end by " + datetime.strftime((datetime.now() + timedelta(hours=meeting_length)), "%H:%M")
        response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

    postSprintGoal()
    postSprintBacklogCards()
    postInProgressCards()
    
    if not current_milestone == None:
        # post cards completed this sprint
        response = urllib2.urlopen("https://api.waffle.io/"+waffle+"/cards/")
        result = response.read()
        decoder = json.JSONDecoder()
        data = decoder.decode(result)
        string = "Stories completed this sprint:\\n"
        for card in data:
            cardFinished = datetime.strptime(card["githubMetadata"]["closed_at"], "%Y-%m-%dT%H:%M:%S.000Z") 
            if card["githubMetadata"]["state"] == "closed" and cardFinished > sprintStart and cardFinished < sprintEnd:
                string += "* " + card["githubMetadata"]["title"] + "\\n"
        response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')
    
    time.sleep(60*60*meeting_length)
    string = "Sprint review meeting time limit expired."
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def startSprintRetrospective():
    string = "Beginning sprint retrospective meeting now."
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')
    current_milestone = getCurrentMilestone()
    if current_milestone == None:
        string = "Cannot estimate recommended sprint retrospective meeting length: current sprint length not found"
    else:
        sprintStart = datetime.strptime(current_milestone['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        sprintEnd = datetime.strptime(current_milestone['due_on'], "%Y-%m-%dT%H:%M:%SZ")
        meeting_length = ((sprintEnd - sprintStart).days + 1) * 2 / 7
        string = "It is recommended that the sprint retrospective meeting last less than " + str(meeting_length) + " hours as there were " + str((sprintEnd - sprintStart).days + 1) + " days in this sprint (using the 2 hours / week of sprint rule).  It should end by " + datetime.strftime((datetime.now() + timedelta(hours=meeting_length)), "%H:%M")
        response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

    postSprintBacklogCards()
    postInProgressCards()

    if not current_milestone == None:
        # count story points completed this sprint
        response = urllib2.urlopen("https://api.waffle.io/"+waffle+"/cards/")
        result = response.read()
        decoder = json.JSONDecoder()
        data = decoder.decode(result)
        size_count = 0
        for card in data:
            cardFinished = datetime.strptime(card["githubMetadata"]["closed_at"], "%Y-%m-%dT%H:%M:%S.000Z") 
            if card["githubMetadata"]["state"] == "closed" and cardFinished > sprintStart and cardFinished < sprintEnd:
                if "size" in card:
                    size_count += card["size"]
        string = "The velocity for this sprint was: " + str(size_count) + " story points / sprint"
        response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')


    time.sleep(60*60*meeting_length)
    string = "Sprint retrospective meeting time limit expired."
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post",  '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')

def post(string):
    response = urllib2.urlopen("https://api.groupme.com/v3/bots/post", '{"text" : "' + string + '", "bot_id" : "' + bot_id + '"}')