from flask import Flask
from flask import request
from posting import *

application = Flask(__name__)


@application.route('/', methods=['POST', 'GET'])
def hello_word():
    if request.method == 'GET':
        post("Scrum bot activated.")
    else:
        text = request.get_json()['text'].lower().strip()
        if text == 'bot, open issues':
            postOpenIssues()
        elif text == 'bot, all cards':
            postAllCards()
        elif text == 'bot, product backlog cards':
            postProductBacklogCards()
        elif text == 'bot, sprint backlog cards':
            postSprintBacklogCards()
        elif text == 'bot, in progress cards':
            postInProgressCards()
        elif text == 'bot, sprint goal':
            postSprintGoal()
        elif text == 'bot, sprint length':
            postSprintLength()
        elif text == 'bot, sprint start':
            postSprintStart()
        elif text == 'bot, sprint end':
            postSprintEnd()
        elif text.startswith('bot, create story'):
            createStory(text[len('bot, create story'):].strip())
        elif text.startswith('bot, move from product backlog to sprint backlog'):
            moveCardProductToSprintBacklog(text[len('bot, move from product backlog to sprint backlog'):].strip())
        elif text.startswith('bot, move from sprint backlog to in progress'):
            moveCardSprintBacklogToInProgress(text[len('bot, move from sprint backlog to in progress'):].strip())
        elif text.startswith('bot, move from in progress to done'):
            moveCardInProgressToDone(text[len('bot, move from in progress to done'):].strip())
        elif text.startswith('bot, set sprint goal'):
            setSprintGoal(text[len('bot, set sprint goal'):].strip())
        elif text.startswith('bot, set sprint end'):
            setSprintEnd(text[len('bot, set sprint end'):].strip())
        elif text == 'bot, start sprint planning meeting':
            startSprintPlanning()
        elif text == 'bot, start daily scrum':
            startDailyScrum()
        elif text == 'bot, start sprint review meeting':
            startSprintReview()
        elif text == 'bot, start sprint retrospective meeting':
            startSprintRetrospective()
        elif text.startswith('bot'):
            post('Unknown command')
    return ""

if __name__ == "__main__":
    application.run()
