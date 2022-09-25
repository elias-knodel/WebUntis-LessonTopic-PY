import time
import requests
import base64
import datetime


# Class Webuntis
#
# This class contains various data and functions for
# interacting with the Webuntis API
#
# Keep in mind that before executing any functions you have to log in
#
# Keep in mind that after executing any functions you have to log out
# You will be automatically logged out in less than 10 minutes by webuntis itself
class Webuntis:
    def __init__(self, username, password, server, school, identity="Awesome"):
        self.username = username
        self.password = password
        self.baseurl = "https://" + server + ".webuntis.com"
        self.school = school
        self.school_base64 = base64.b64encode(school.encode('ascii'))
        self.id = identity
        self.sessionInformation = {}
        self.headers = None

    # Generates needed cookies for session authentication
    def generate_headers(self, cookies):
        cookies_array = [
            'JSESSIONID=' + cookies['JSESSIONID'],
            'schoolname=' + cookies['schoolname']
        ]
        seperator = "; "
        cookies_string = seperator.join(cookies_array)
        headers = {
            "cookie": cookies_string,
            "Content-Type": "application/json"
        }
        self.headers = headers

    # Connects the client to the specified webuntis server
    def login(self):
        url = self.baseurl + "/WebUntis/jsonrpc.do"
        querystring = {
            "school": self.school
        }
        payload = {
            "id": self.id,
            "method": "authenticate",
            "params": {
                "user": self.username,
                "password": self.password,
                "client": self.id
            },
            "jsonrpc": "2.0"
        }
        res = requests.request("POST", url, json=payload, params=querystring)
        self.sessionInformation = res.json()['result']
        self.generate_headers(res.cookies)

        if res.json()['result']['sessionId'] is not None:
            print("Success! User has been logged in!")
            return True
        else:
            print("Error! User login failed!")
            return False

    # Disconnects the client from the specified webuntis server
    def logout(self):
        url = self.baseurl + "/WebUntis/jsonrpc.do"
        querystring = {
            "school": self.school
        }
        payload = {
            "id": self.id,
            "method": "logout",
            "params": {},
            "jsonrpc": "2.0"
        }
        res = requests.request("POST", url, json=payload, params=querystring, headers=self.headers)
        self.sessionInformation = None

        if res.json()['result'] is not None:
            print("Error! User logout failed!")
            return False
        else:
            print("Success! User has been logged off!")
            return True

    # This is a general request just change the untis_method
    #
    # Some Examples you can call are:
    #   - getSchoolyears
    #   - getLatestImportTime
    #   - getSubjects
    #   - getTimegridUnits
    #   - getTeachers
    #   - getStudents
    #   - getRooms
    #   - getKlassen
    #   - getDepartments
    #   - getHolidays
    #   - getStatusData
    #
    def generate_request(self, rest_method="POST", untis_method="getHolidays", url='/WebUntis/jsonrpc.do',
                         parameter=None):
        if parameter is None:
            parameter = {}
        url = self.baseurl + url
        querystring = {
            'school': self.school
        }
        payload = {
            "id": self.id,
            "method": untis_method,
            "params": parameter,
            "jsonrpc": "2.0"
        }

        return requests.request(method=rest_method, url=url, json=payload, headers=self.headers, params=querystring)

    def timetable_request(self, start_date, end_date):
        parameter = {
            "options": {
                "id": int(time.time() * 1000),
                "element": {
                    "id": self.sessionInformation["personId"],
                    "type": self.sessionInformation["personType"]
                },
                "startDate": start_date,
                "endDate": end_date,
                "showLsText": True,
                "showStudentgroup": True,
                "showLsNumber": True,
                "showSubstText": True,
                "showInfo": True,
                "showBooking": True,
                "klasseFields": ['id', 'name', 'longname', 'externalkey'],
                "roomFields": ['id', 'name', 'longname', 'externalkey'],
                "subjectFields": ['id', 'name', 'longname', 'externalkey'],
                "teacherFields": ['id', 'name', 'longname', 'externalkey'],
            }
        }
        res = self.generate_request(untis_method="getTimetable", parameter=parameter)

        return res

    def get_all_lessons(self):
        res = self.generate_request(rest_method="GET", untis_method="getSchoolyears")
        school_years = res.json()['result']

        timetables = []

        for year in school_years:
            res = self.timetable_request(year['startDate'], year['endDate'])
            if res:
                if res.json():
                    if res.json()['result']:
                        timetables.append(res.json()['result'])

        return timetables

    def get_lesson_topic(self, lesson):
        parameter = {}
        url = self.baseurl + "/WebUntis/api/public/period/info"
        querystring = {
            'school': self.school,
            "date": lesson["date"],
            "starttime": lesson["startTime"],
            "endtime": lesson["endTime"],
            "elemid": self.sessionInformation["personId"],
            "elemtype": self.sessionInformation["personType"],
            "ttFmtId": "1",
            "selectedPeriodId": lesson["id"],
        }
        payload = {
            "id": self.id,
            "params": parameter,
            "jsonrpc": "2.0"
        }
        res = requests.request(method="GET", url=url, json=payload, headers=self.headers, params=querystring)

        lesson_dict = {
            "startTime": lesson["startTime"],
            "subject": "",
            "subjectLong": "",
            "topic": ""
        }

        res_data = res.json()["data"]
        if res_data["blocks"]:
            for block in res_data["blocks"]:
                for lesson in block:
                    if lesson["subjectName"]:
                        lesson_dict["subject"] = lesson["subjectName"]
                    if lesson["subjectNameLong"]:
                        lesson_dict["subjectLong"] = lesson["subjectNameLong"]
                    if lesson["lessonTopic"]:
                        lesson_dict["topic"] = lesson["lessonTopic"]["text"]
                    return lesson_dict
