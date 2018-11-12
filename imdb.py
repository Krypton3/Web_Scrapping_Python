from bs4 import BeautifulSoup
import requests
import json
import re
import csv


id = ['0371746', '0800080', '1228705', '0800369', '0458339', '0848228', '1300854', '1981115', '1843866', '2015381',
      '2395427', '0478970', '3498820', '1211837', '3896198', '3501632', '2250912', '1825683', '4154756', '5095030']

# id = ['5095030']
with open('marvel.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['movie_name', 'movie_year', 'movie_rating_type', 'movie_description', 'movie_keywords',
                     'movie_genre', 'movie_actors', 'movie_rating_user', 'movie_rating', 'direction', 'writers',
                     'storyline', 'movie_runtime'])

    track = 0
    while track < len(id):
        page_link = "http://www.imdb.com/title/tt"+str(id[track])
        page_response = requests.get(page_link, timeout=5)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        data = json.loads(page_content.find('script', type='application/ld+json').text)

        get = page_content.find('span', attrs={"id": "titleYear"})
        movie_year = get.text
        movie_year = re.sub(r"(\()", r"", movie_year)
        movie_year = re.sub(r"(\))", r"", movie_year)
        movie_year = re.sub(r"(\s+)", r"", movie_year)

        if (int(movie_year) >= 2000) and (int(movie_year) <= 2018):

            check = page_content.find('div', attrs={"class": "title_wrapper"})
            check1 = check.findAll('a')
            get_year_origin = check1[len(check1)-1].text.split(" ")
            print(get_year_origin)
            check_year = get_year_origin[2]
            check_origin = get_year_origin[3]
            check_origin = re.sub(r"(\()", r"", check_origin)
            check_origin = re.sub(r"(\))", r"", check_origin)
            check_origin = re.sub(r"(\s+)", r"", check_origin)
            print(check_year)
            print(check_origin)

            if  check_origin == 'USA' or check_origin == 'Bangladesh':
                movie_name = data['name']
                movie_rating_type = data['contentRating']
                movie_description = data['description']
                movie_keywords = data['keywords']
                movie_genre = data['genre']
                movie_actors = len(data['actor'])
                movie_rating_user = data['aggregateRating']['ratingCount']
                movie_rating = data['aggregateRating']['ratingValue']

                i = 0
                stars = []
                while i < movie_actors:
                    stars.append(data['actor'][i]['name'])
                    i = i + 1

                direction = []
                if type(data['director']) == list:
                    dict = len(data['director'])
                    i = 0
                    while i < dict:
                        if 'name' in data['director'][i]:
                            direction.append(data['director'][i]['name'])
                        i = i + 1
                else:
                    direction.append(data['director']['name'])

                writers = []
                if type(data['creator']) == list:
                    dict = len(data['creator'])
                    i = 0
                    while i < dict:
                        if 'name' in data['creator'][i]:
                            writers.append(data['creator'][i]['name'])
                        i = i + 1
                else:
                    writers.append(data['creator']['name'])

                primary = page_content.find('div', attrs={"class": "title_wrapper"})

                # extracting runtime
                genre_runtime = primary.find('div', attrs={"class": "subtext"}).text.split("|")
                movie_runtime = re.sub(r"(\s+)", r"", genre_runtime[1])

                get = page_content.find('div', attrs={"class": "inline canwrap"})
                storyline = get.find('span').text

                writer.writerow([movie_name, movie_year, movie_rating_type, movie_description, movie_keywords, movie_genre,
                                stars, movie_rating_user, movie_rating, direction, writers, storyline, movie_runtime])
                print(track)

        track = track + 1


