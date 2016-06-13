# Nicholas Dry http://www.nicholasdry.com
# Copyright 2016

# TODO: Allow for the checking of more than one class

from bs4 import BeautifulSoup   # This module allows for the scraping of the website.
from selenium import webdriver  # This module allows for the authentication through websites.
import time # This module allows for the sleep function to be called.
import os
import sys

pastTextFile = []
current = []

# TODO: Saving of a list into a text file, then loading it back into a dictionary
# This method pulls a past text file called past.txt and saves it into a list,
def loadPastTextFile():
    with open('past.txt') as f:
        pastTextFile.append(f.read().split())

def checkSimilarity():
    if current == pastTextFile:
        print("same")
    else:
        print("not same")

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
    return 0

# This method handles if the iframe is Gradebook.
# Gradebook page title is "Gradebook Tool"
def gradebookOne():
    assignmentNames = gradebook.find_all("td", {"class": "left"}) # This grabs the assignment names
    assignmentGrades = gradebook.find_all("td", {"class": "center"}) # This grabs the assignment names

    gradeDictionary = {}

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

    past = open("current.txt", "w")
    for i in current:
        past.write("%s\n" % i)

    with open('current.txt') as f:
        current.append(f.read().split())



loadPastTextFile()

attempts = 0

while attempts < 3:
    try:
        driver = webdriver.Firefox()  # PhantomJS allows the script to run without opening up Firefox or any browser
        driver.get("https://cas.rutgers.edu/login?service=https%3A%2F%2Fsakai.rutgers.edu%2Fsakai-login-tool%2Fcontainer")  # This is the sakai homepage

        username_field = driver.find_element_by_name("username") # Sakai nicely names its fields.
        password_field = driver.find_element_by_name("password")
        username_field.send_keys("nsd48") # User NetID
        password_field.send_keys("Mustafa12578") # User
        password_field.submit() # submit it

        # This is the gradebook which are attempting to access
        driver.get("https://sakai.rutgers.edu/portal/site/7d6cf024-b944-4e38-a21a-06f73f427ce4/page/fedd6c39-4d6a-4a46-8a2f-f8aaf97b5df4")
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

# TODO: Send notification, Title = Class Name, Subtitle = Assignment Name, Message = Assignment Grade
checkSimilarity()
