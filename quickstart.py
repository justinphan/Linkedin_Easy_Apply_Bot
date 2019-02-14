from easyapplybot import EasyApplyBot
# from easyapplybot_Premium import EasyApplyBot

import loginGUI

"""
define if ou want to use the GUI or not (True or False)

"""
useGUI = False


"""
If GUI is False enter your credentials and preferences manually
"""

if useGUI == False :

    username = 'abcsd@gmail.com' # LinkedIn Username
    password = 'mypassword1234' # LinkedIn Password
    language = 'en' # LinkedIn default language (en, es, pt)
    position = 'Software Engineer' # Job position
    location = 'New York, New York' # location where to apply (e.g. Barcelona)
    resumeloctn = ''  # Directory path where your document is


"""
If GUI is True, just run the script
"""

if useGUI == True :

    app = loginGUI.LoginGUI()
    app.mainloop()

    # get user info info
    username=app.frames["StartPage"].username
    password=app.frames["StartPage"].password
    language=app.frames["PageOne"].language
    position=app.frames["PageTwo"].position
    location_code=app.frames["PageThree"].location_code
    if location_code == 1:
        location=app.frames["PageThree"].location
    else:
        location = app.frames["PageFour"].location
    resumeloctn=app.frames["PageFive"].resumeloctn

    print(username,password, language, position, location_code, location, resumeloctn)


#start bot
bot = EasyApplyBot(username,password, language, position, location, resumeloctn)
bot.start_apply(position, location, resumeloctn)
