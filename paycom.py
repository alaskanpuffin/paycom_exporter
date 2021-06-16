import mechanicalsoup
import json
from datetime import datetime, timezone, timedelta

class Paycom():
    def __init__(self):
        self.paycom = {}
        self.browser = mechanicalsoup.StatefulBrowser()

    def signIn(self, username, password, code, securityquestion):
        self.browser.open("https://www.paycomonline.net/v4/cl/cl-login.php")

        self.browser.select_form("[name=frmClLogin]")

        self.browser["clientcode"] = code
        self.browser["username"] = username
        self.browser["password"] = password

        self.browser.submit_selected()

        self.browser.open("https://www.paycomonline.net/v4/cl/web.php/security/security-question/login?session_nonce=")

        self.browser.select_form()

        self.browser["firstSecurityQuestion"] = securityquestion
        self.browser["secondSecurityQuestion"] = securityquestion

        self.browser.submit_selected()

    def scrapeLastSync(self, target):
        clockDict = {}

        self.browser.open("https://www.paycomonline.net/v4/cl/web.php/ta/androidterminal/dashboard")

        postData = {"draw": "1"}
        postHeader = {"X-Requested-With": "XMLHttpRequest"}
        
        clockData = self.browser.post("https://www.paycomonline.net/v4/cl/web.php/ta/androidterminal/dashboardData", data=postData, headers=postHeader)
        clockJson = json.loads(clockData.text)

        for clock in clockJson['data']:
            if clock['serialNumber'] == target:
                clockDict = clock
                break

        currentTime = datetime.now(timezone(timedelta(hours=-5))).replace(tzinfo=None)
        lastSync = datetime.strptime(clockDict['lastSync'], "%m/%d/%y %I:%M %p")
        lastSeen = datetime.strptime(clockDict['lastSeen'], "%m/%d/%y %I:%M %p")

        self.paycom['lastsync'] = clockDict['lastSync']
        self.paycom['lastseen'] = clockDict['lastSeen']
        self.paycom['lastsyncseconds'] = (currentTime - lastSync).total_seconds()
        self.paycom['lastseenseconds'] = (currentTime - lastSeen).total_seconds()

        resp = ''
        for key, value in self.paycom.items():
            resp = resp + ("paycom_%s %s \n" % (key, value))

        return resp


    def getLastSync(self, username, password, code, securityquestion, target):
        self.signIn(username, password, code, securityquestion)

        return self.scrapeLastSync(target)