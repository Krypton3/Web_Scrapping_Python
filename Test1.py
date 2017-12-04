import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.yellowpages.com/search?search_terms=coffee&geo_location_terms=Los+Angeles%2C+CA"
url_pages = url + '&page=' + str(2) + '&s=relevance'

i = 1
while i < 10:
    if i == 1:
        url_final = url
    else:
        url_final = url + '&page=' + str(i) + '&s=relevance'
    i = i + 1
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    links = soup.find_all("a")

    # for link in links:
    #    print("<a href='%s'>%s</a>" % (link.get("href"), link.text))

    data = soup.find_all("div", {"class": "info"})

    # for item in data:
    # print(item.contents[0].text)
    # print(item.contents[1].text)
    # print(("Business Name: %s") % (item.contents[0].find_all("a", {"class": "business-name"})[0].text))
    # print(("Rating: %s") % (item.contents[1].find_all("a", {"class": "rating"})[0].text))
    # print(("Address: %s") % (item.contents[1].find_all("p", {"class": "adr"})[0].text))
    # print(("Phone Number: %s") % (item.contents[1].find_all("div", {"class": "phones"})[0].text))
    # print(("Category: %s") % (item.contents[2].find_all("div", {"class": "categories"})[0].text))

    # use try catch to avoid the error
    with open('coffee.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Business Name', 'Address', 'Phone Number', 'Category'])
        for item in data:
            filewriter.writerow([str(item.contents[0].find_all("a", {"class": "business-name"})[0].text),
                                 str(item.contents[1].find_all("p", {"class": "adr"})[0].text),
                                 str(item.contents[1].find_all("div", {"class": "phones"})[0].text),
                                 str(item.contents[2].find_all("div", {"class": "categories"})[0].text)])
