# Sakai-Grade-Checker

A python script for Rutgers students which checks a specific gradebook at a certain time interval and notifies the student by text message, email, or macOS notificiation if their grade has changed.

# Requirements

In order to use the Firefox driver for this script, you need an older version of Firefox, I recommend 24.0 because it is compatible with Selenium.

[a link](https://ftp.mozilla.org/pub/firefox/releases/24.0/)

The dependencies needed are:
Selenium (for web authentication)
```
pip install selenium
```
BeautifulSoup (for web scraping)
```
pip install BeautifulSoup
```
Twilio REST API (for text messages)
```
pip install twilio
```
