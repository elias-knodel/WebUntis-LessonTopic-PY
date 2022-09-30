# WebUntis API for Lessontopics in Python

[![gh-commit-badge][gh-commit-badge]][gh-commit]
[![gh-contributors-badge][gh-contributors-badge]][gh-contributors]
[![gh-stars-badge][gh-stars-badge]][gh-stars]

## Description

I don't like python but oh well here I am...  
This was made entirely in my free time and is in no way associated with any business.  
It is my first python project so mistakes can happen so please keep that in mind.

## Getting started

1. Copy env file

```shell
cp .env.example .env
```

2. Fill in your login credentials into the `.env` file.  
   (Don't worry, the `.env` does not get committed so your secrets are safe there)

3. If you want an example of how this works go to [/webuntis_example.py](/webuntis_example.py)

## How to use

### In code

```python
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

# Log the client out
client.logout()

# Now you can access the data by reading the cache
cacheLT.read()
```

### Data Structure

So you can access the lesson topics with `cacheLT.read()` now... But what does it return?

Here is an example:

```json
{
    "20220919": [
        {
            "startTime": 925,
            "subject": "D",
            "subjectLong": "Deutsch",
            "topic": "Aufgaben"
        },
        {
            "startTime": 1010,
            "subject": "E",
            "subjectLong": "Englisch",
            "topic": "Assignments"
        }
    ]
}
```

## Contributing

If you want to take part in contribution, like fixing issues and contributing directly to the code base, plase visit
the [How to Contribute][gh-contribute] document.

## Useful links

[License][gh-license] -
[Contributing][gh-contribute] -
[Code of conduct][gh-codeofconduct] -
[Issues][gh-issues] -
[Pull requests][gh-pulls]

<hr>  

###### Copyright (c) [Elias Knodel][gh-team]. All rights reserved | Licensed under the MIT license.

<!-- Variables -->

[gh-commit-badge]: https://img.shields.io/github/last-commit/elias-knodel/webuntis-lessontopic-py?style=for-the-badge&colorA=302D41&colorB=cba6f7

[gh-commit]: https://github.com/elias-knodel/webuntis-lessontopic-py/commits/main

[gh-contributors-badge]: https://img.shields.io/github/contributors/elias-knodel/webuntis-lessontopic-py?style=for-the-badge&colorA=302D41&colorB=89dceb

[gh-contributors]: https://github.com/elias-knodel/webuntis-lessontopic-py/graphs/contributors

[gh-stars-badge]: https://img.shields.io/github/stars/elias-knodel/webuntis-lessontopic-py?style=for-the-badge&colorA=302D41&colorB=f9e2af

[gh-stars]: https://github.com/elias-knodel/webuntis-lessontopic-py/stargazers

[gh-contribute]: https://github.com/elias-knodel/webuntis-lessontopic-py/blob/main/CONTRIBUTING.md

[gh-license]: https://github.com/elias-knodel/webuntis-lessontopic-py/blob/main/LICENSE

[gh-codeofconduct]: https://github.com/elias-knodel/webuntis-lessontopic-py/blob/main/CODE_OF_CONDUCT.md

[gh-issues]: https://github.com/elias-knodel/webuntis-lessontopic-py/issues

[gh-pulls]: https://github.com/elias-knodel/webuntis-lessontopic-py/pulls

[gh-team]: https://github.com/elias-knodel
