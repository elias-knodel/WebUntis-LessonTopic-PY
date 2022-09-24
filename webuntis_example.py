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

#############################################
#                                           #
# The main part will be here (lessontopic)  #
#                                           #
#############################################
cacheLT = cache.Cache("lessontopic")
isValidLT = cacheLT.verify()
# if not isValidLT:
lesson_topics = client.get_lesson_topics()
cacheLT.write(json_data=lesson_topics)
#############################################
#                                           #
#############################################

# Log the client out
client.logout()
