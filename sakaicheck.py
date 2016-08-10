# Nicholas Dry http://www.nicholasdry.com

# TODO: Allow for the checking of more than one class
# TODO: Implement API for email updates if grade updates

from bs4 import BeautifulSoup
from selenium import webdriver
from twilio.rest import TwilioRestClient
import time
import os
import os.path
import sys

##########################################################################
# BELOW ARE THE VARIABLES WHICH NEED TO BE ALTERED DEPENDING ON THE USER.#
##########################################################################

netID = ""
netIDPassword = ""

# Haven't made use of an email API yet.
userEmail = "nicholasdry@me.com"
userCellPhone = +18563258310

# These are boolean values to change to determine which updates you would like to recieve.
# By default these are all set to False.
smsAlert = True
iosAlert = True
emailAlert = False

# These variables hold a list style of all the information per class
pastTextFile = []
currentTextFile = []
current = []
dontNotify = False

className = ""

# This method is called at the end of the program to copy the new current into
# past.txt and remove current.txt
def cleanUp():
    past = open("past.txt", "w")
    for i in current:
        past.write("%s\n" % i)

    os.remove("current.txt")

# This method pulls a past text file called past.txt and saves it into a list,
def loadPastTextFile():
    with open('past.txt') as f:
        pastTextFile.append(f.read().split())

# This method pulls the current text file which is being worked on.
def loadCurrentTextFile():
    with open('current.txt') as f:
        currentTextFile.append(f.read().split())

# This method is called to compare the gradebook files and direct the program from there.
def checkSimilarity():
    if currentTextFile == pastTextFile:
        exit()
    else:
        if dontNotify:
            sendNotification("Sakai Grade Checker", "Course Installation Complete", "Thanks for using!")
            cleanUp()
            exit()
        if smsAlert:
            sendTextMessage()
        if iosAlert:
            sendNotification("{}".format(className[20:len(className)-12]), "Grade Update", "Your grade has been updated.")
        if emailAlert:
            sendEmail()
        else:
            print("Your {} grade has been updated.".format(className[20:len(className)-12]))
        cleanUp()

# This method is for anyone on Mac OSX who wishes to receive notifications of when the grades are posted through Notification Center.
def sendNotification(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system("terminal-notifier {}".format(' '.join([t, s, m])))

# This method is for anyone who wishes to receive notifications of when the grades are posted through email.
def sendEmail():
    return 0

# This method is for anyone who wishes to recieve text notifications of grade changes.
def sendTextMessage():
    # My Twilio credentials
    ACCOUNT_SID = "changeMe"
    AUTH_TOKEN = "changeMe"

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    client.messages.create(
    		to=userCellPhone,
        	from_="+18566197129",
        	body="Your {} grade has been updated.".format(className[20:len(className)-12]),
    )

# This method handles if the iframe is Gradebook.
# Gradebook page title is "Gradebook Tool"
def gradebookOne():
    assignmentNames = gradebook.find_all("td", {"class": "left"}) # This grabs the assignment names
    assignmentGrades = gradebook.find_all("td", {"class": "center"}) # This grabs the assignment names

    for i in assignmentNames:
        current.append(i)

    for i in assignmentGrades:
        current.append(i)

    outputToCurrent = open("current.txt", "w")
    for i in current:
        outputToCurrent.write("%s\n" % i)

# This method handles if the iframe is Gradebook 2.
# Gradebook 2 page title is "Gradebook"
def gradebookTwo():
    assignmentNames = gradebook.find_all("div", {"class": "x-grid3-cell-inner x-grid3-col-S_ITM_NM"}) # This grabs the assignment names
    assignmentGrades = gradebook.find_all("div", {"class": "x-grid3-cell-inner x-grid3-col-S_GRD"}) # This grads the assignment grades

    for i in assignmentNames:
        current.append(i)

    for i in assignmentGrades:
        current.append(i)

    outputToCurrent = open("current.txt", "w")
    for i in current:
        outputToCurrent.write("%s\n" % i)

# This determines if past.txt exists or not
if not os.path.isfile("past.txt"):
    f = open("past.txt", "w")
    dontNotify = True

loadPastTextFile()

attempts = 0

while attempts < 3:
    try:
        # PhantomJS allows the script to run without opening up Firefox or any browser.
        # You can also use webdriver.Firefox() but it will open up a browser window
        driver = webdriver.Firefox()
        driver.get("https://cas.rutgers.edu/login?service=https%3A%2F%2Fsakai.rutgers.edu%2Fsakai-login-tool%2Fcontainer")  # This is the sakai homepage

        username_field = driver.find_element_by_name("username")
        password_field = driver.find_element_by_name("password")
        username_field.send_keys(netID)
        password_field.send_keys(netIDPassword)
        password_field.submit()

        # This are the gradebooks I have tried on mine.
        # Data 101: https://sakai.rutgers.edu/portal/site/848d9ee2-3e91-4935-bed6-ac8e4c77f22c/page/9f5d49e0-8574-4395-b192-65b0b52780ec
        # Intl Econ: https://sakai.rutgers.edu/portal/site/8f1472b9-9413-4795-99d5-fd1fa81b17c3/page/9fc30ca2-3349-4a21-85df-0cf6e69481bd
        # Comp Arch: https://sakai.rutgers.edu/portal/site/7d6cf024-b944-4e38-a21a-06f73f427ce4/page/fedd6c39-4d6a-4a46-8a2f-f8aaf97b5df4
        # Disc Stru: https://sakai.rutgers.edu/portal/site/3c91ebbf-3c52-4572-98f9-899a77c7f227/page/301b5faf-8f77-4f4a-a282-e44edc801f3d


        driver.get("https://sakai.rutgers.edu/portal/site/bf9592a4-b085-4547-9bd9-a3e286b0de28/page/395bd314-6b4a-4336-ae31-4230a26a0b31")
	break
    except:
        print("Trying again to locate element.")
        attempts = attempts + 1


if attempts == 3:
    sendNotification("ERROR", "Unable to Connect to Sakai", "Internet Connection Not Available")
    exit()

# This section simply grabs the title of the class in order to clean up the notifications.
html = driver.page_source
justForTitle = BeautifulSoup(html, "html.parser")
className = justForTitle.title.string

time.sleep(10)

frame = driver.find_element_by_tag_name("iframe")   # We want to grab the iframe.
driver.switch_to_frame(frame)   # Now we send our driver to that new frame which allows us to access the page source below.

time.sleep(6)   # Since the gradebook must load, we allow it to wait six seconds.

html = driver.page_source   # Grab the source code the the iframe widget.
gradebook = BeautifulSoup(html, "html.parser")  # Begin the segmenting and parsing.

# This determines what version gradebook Sakai is using.
if gradebook.title.string == "Gradebook":
    gradebookTwo()
else:
    gradebookOne()

# Loads the file into a list so we can check.
loadCurrentTextFile()

# Checks for similarities.
checkSimilarity()
