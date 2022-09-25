import webuntis
import cache
from decouple import config

# Get login credentials from env file
username = config('USERNAME')
password = config('PASSWORD')
server = config('SERVER')
school = config('SCHOOL')

# Create WebUntis API Wrapper Object
client = webuntis.Webuntis(username, password, server, school)

# Log the client in webuntis
client.login()

# Generate a basic query which will return its result (Response)
holidays = client.generate_request(rest_method='GET')

# Create a Cache so that large data queries will only get fired once a day
cacheC = cache.Cache("classes")
isValidC = cacheC.verify()

if not isValidC:
    classes = client.generate_request(rest_method='GET', untis_method="getKlassen")
    cacheC.write(json_data=classes.json()['result'])

#################################################
#                                               #
# The main function will be here (lessontopic)  #
#                                               #
#################################################
# This gets all lessons in all your school-years and saves them into a cache file
cacheL = cache.Cache("lessons")
isValidLT = cacheL.verify()

if not isValidLT:
    lessons = client.get_all_lessons()
    cacheL.write(json_data=lessons)

# This gets all lessons in a day in all years and loops over them
# Then it saves the topics of each lesson into a cache file
cacheLT = cache.Cache("lessontopics")
isValidLT = cacheLT.verify()

if not isValidLT:
    lesson_topic_dict = {}

    for year in cacheL.read():
        for lesson in year:
            index_day = lesson["date"]
            index_lesson = lesson["startTime"]

            if lesson_topic_dict.get(index_day) is None:
                lesson_topic_dict[index_day] = []

            lesson_topic_dict[index_day].append(client.get_lesson_topic(lesson))

    cacheLT.write(json_data=lesson_topic_dict)
#################################################
#                                               #
#################################################

# Log the client out
client.logout()
