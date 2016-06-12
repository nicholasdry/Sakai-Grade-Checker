

from bs4 import BeautifulSoup
from selenium import webdriver
import urllib2
import time

driver = webdriver.Firefox()  # PhantomJS allows the script to run without opening up Firefox or any browser
driver.get("https://cas.rutgers.edu/login?service=https%3A%2F%2Fsakai.rutgers.edu%2Fsakai-login-tool%2Fcontainer")  # This is the sakai homepage

username_field = driver.find_element_by_name("username") # Sakai nicely names its fields.
password_field = driver.find_element_by_name("password")
username_field.send_keys("nsd48") # User NetID
password_field.send_keys("Mustafa12578") # User
password_field.submit() # submit it

driver.get("https://sakai.rutgers.edu/portal/site/7d6cf024-b944-4e38-a21a-06f73f427ce4/page/fedd6c39-4d6a-4a46-8a2f-f8aaf97b5df4")

frame = driver.find_element_by_tag_name("iframe")
driver.switch_to_frame(frame)

time.sleep(6)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

print(soup) # now prettify it!



# For assignment names we want to search for: x-grid3-cell-inner x-grid3-col-S_ITM_NM
# For assignment grades we want to search for: x-grid3-cell-inner x-grid3-col-S_GRD

f.close()
