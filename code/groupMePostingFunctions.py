import urllib2
import json
from operator import itemgetter

githubRepo = "grahamheather/CS4320FinalProject"
waffle = "grahamheather/CS4320FinalProject"

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
