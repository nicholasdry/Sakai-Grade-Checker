# Nicholas Dry http://www.nicholasdry.com

# TODO: Allow for the checking of more than one class
# TODO: Check if the past.txt file exists, if not, create and load the first scrape into it
# TODO: Implement API for email updates if grade updates

from bs4 import BeautifulSoup
from selenium import webdriver  # This module allows for the authentication through websites.
from twilio.rest import TwilioRestClient
import time
import os
import os.path
import sys

##########################################################################
# BELOW ARE THE VARIABLES WHICH NEED TO BE ALTERED DEPENDING ON THE USER.#
##########################################################################

netID = "nsd48"
netIDPassword = "Mustafa12578"
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

# This method is called at the end of the program to copy the new current into
# past.txt and remove current.txt
def cleanUp():
    past = open("past.txt", "w")
    for i in current:
        past.write("%s\n" % i)

    os.remove("current.txt")

# TODO: Saving of a list into a text file, then loading it back into a dictionary
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
    # TODO: Now we have to update the "past.txt" file since we have a new standard to check against.
    else:
        if smsAlert:
            sendTextMessage()
        if iosAlert:
            sendNotification("Sakai Grade Checker", "Grade Update", "Your grade has been updated.")
        if emailAlert:
            sendEmail()
        else:
            print("Your grade has been updated.")
        cleanUp()

# This method is called in order to write the new past file.
# IN DEVELOPMENT
def createNewPast():

    sys.exit()
    return 0

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
# TODO: Scrape for the name of the class which the grade has been updated.
def sendTextMessage():
    # put your own credentials here
    ACCOUNT_SID = "AC684184f26e7ac3088a17c73be11536a8"
    AUTH_TOKEN = "e0f237315288cc5ca43eb30e3d2655b5"

    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    client.messages.create(
    		to=userCellPhone,
        	from_="+18566197129",
        	body="Your grade has been updated.",
    )

# This method handles if the iframe is Gradebook.
# Gradebook page title is "Gradebook Tool"
def gradebookOne():
    assignmentNames = gradebook.find_all("td", {"class": "left"}) # This grabs the assignment names
    assignmentGrades = gradebook.find_all("td", {"class": "center"}) # This grabs the assignment names

    gradeDictionary = {}

    # TODO: Edit the below methods to look similar to Gradebook 2 since we are simply checking smaller
    # chunks of HTML now.
    count = 0

    for i in assignmentNames:
        list = []
        for j in range(0, 3):
            list[j] = assignmentGrades[count]
            count = count + 1
        gradeDictionary[i.get_tex()] = list

    print(gradeDictionary)

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

if os.path.isfile("past.txt"):
    loadPastTextFile()
# TODO: Finish method below.
else:
    createNewPast()

attempts = 0
while attempts < 3:
    try:
        # PhantomJS allows the script to run without opening up Firefox or any browser.
        driver = webdriver.PhantomJS()
        driver.get("https://cas.rutgers.edu/login?service=https%3A%2F%2Fsakai.rutgers.edu%2Fsakai-login-tool%2Fcontainer")  # This is the sakai homepage

        username_field = driver.find_element_by_name("username")
        password_field = driver.find_element_by_name("password")
        username_field.send_keys(netID)
        password_field.send_keys(netIDPassword)
        password_field.submit()

        # This is the gradebook which are attempting to access.
        driver.get("https://sakai.rutgers.edu/portal/site/3c91ebbf-3c52-4572-98f9-899a77c7f227/page/301b5faf-8f77-4f4a-a282-e44edc801f3d")
        break
    except:
        print("Connection Error: Trying Again")
        attempts = attempts + 1

if attempts == 3:
    sendNotification("ERROR", "Unable to Connect to Sakai", "Internet Connection Not Available")
    exit()

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

loadCurrentTextFile()

checkSimilarity()
