# Using the Scrum Bot
## Set up
  - Create a server running Flask and upload the code
  - Create a bot at https://dev.groupme.com
    - Add the bot to the desired GroupMe chat
    - Set the callback URL to the server
  - In GitHub, Settings > Developer Settings > Personal access tokens
    - Generate a token
    - For permissions, mark ```public_repo```
  - In the config file (config.py):
    - Set```bot_id``` to the GroupMe Bot ID
    - Set ```githubRepo``` to the desired GitHub repo in the form [owner's username]/[repo name]
    - Set ```waffle``` to the project's board on Waffle in the form [owner's name]/[project name]
    - Set ```githubOAuth``` to the GitHub personal access token previously generated
  - The bot should now be functional

## Use
Valid commands:
  - "Bot, open issues"
  - "Bot, all cards"
  - "Bot, product backlog cards"
  - "Bot, sprint backlog cards"
  - "Bot, in progress cards"
  - "Bot, sprint goal"
  - "Bot, sprint length"
  - "Bot, sprint start"
  - "Bot, sprint end"
  - "Bot, create story [story name]"
  - "Bot, move from product backlog to sprint backlog [story name]"
  - "Bot, move from sprint backlog to in progress [story name]"
  - "Bot, move from in progress to done [story name]"
  - "Bot, set sprint goal [sprint goal text]"
  - "Bot, set sprint end [MM/DD/YYYY]"
  - "Bot, start sprint planning meeting"
  - "Bot, start daily scrum"
  - "Bot, start sprint review meeting"
  - "Bot, start sprint retrospective meeting"
