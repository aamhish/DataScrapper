import requests
import csv
import re
from bs4 import BeautifulSoup
state_list = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
	"Connecticut","Delaware","Florida","Georgia (U.S. state)","Hawaii","Idaho","Illinois",
	"Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
	"Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
	"Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York (state)",
	"North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
	"Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
	"Vermont","Virginia","Washington (state)","West Virginia","Wisconsin","Wyoming"] #can be used to get rid of the state pages
state_list_nospace = ["/Alabama","/Alaska","/Arizona","/Arkansas","/California","/Colorado",
	"/Connecticut","/Delaware","/Florida","/Georgia_(U.S._state)","/Hawaii","/Idaho","/Illinois",
	"/Indiana","/Iowa","/Kansas","/Kentucky","/Louisiana","/Maine","/Maryland",
	"/Massachusetts","/Michigan","/Minnesota","/Mississippi","/Missouri","/Montana",
	"/Nebraska","/Nevada","/New_Hampshire","/New_Jersey","/New_Mexico","/New_York_(state)",
	"/North_Carolina","/North_Dakota","/Ohio","/Oklahoma","/Oregon","/Pennsylvania",
	"/Rhode_Island","/South_Carolina","/South_Dakota","/Tennessee","/Texas","/Utah",
	"/Vermont","/Virginia","/Washington_(state)","/West_Virginia","/Wisconsin","/Wyoming"]#can be used to get rid of the state pages

print("INIT")
url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
page = requests.get(url).text

souped_page = BeautifulSoup(page, 'html.parser')

table_of_data = souped_page.find('table', {'class': 'wikitable sortable'})
#some typical init

city_list = []
link_list = []
links = table_of_data.findAll('a') #looking for the links
count = 1;
for link in links:
		city_list.append(link.get('title')) #getting the real stuff
		if (not(link.get('href').find('/wiki')==-1) and not(any(x in link.get('href') for x in state_list_nospace)) or "/wiki/Indianapolis" in link.get('href')or "/wiki/Oklahoma_City" in link.get('href')or "/wiki/Kansas_City" in link.get('href')or "/wiki/Virginia_Beach" in link.get('href')or "/wiki/Colorado_Springs" in link.get('href')):
			link_list.append("https://en.wikipedia.org"+link.get('href')) #these cities up hear made the whole process annoying and should seriously consider renaming their city /s
clean_link_list = []

clean_city_list=[]
cleaned_city_list=[];
#checks if the thing is in the state list and so is not a link we want
for link in city_list:
	if(not(link==None or [x for x in state_list if link in x])):
		clean_city_list.append(link)

#puts the cities and links in a nice dict
city_site_dict = dict(zip(clean_city_list, link_list))

#print(clean_city_list)
#print(city_site_dict)

with open('newesttest.csv', 'a') as csvFile:
	#goes through putting stuff in csvs and scraps the image links and puts that in the excel file too
	writer = csv.writer(csvFile)
	writer.writerow(["City", "Link", "Images"])
	for x in city_site_dict:
		url = x
		page = requests.get(city_site_dict[url]).text
		souped_page = BeautifulSoup(page, 'html.parser')
		images = souped_page.find_all('img', {'src':re.compile('.jpg')})
		y = []
		for image in images:
			y.append(str(image['src']))
		
		writer.writerow([x, city_site_dict[x], ",".join(y).replace('"', '')])
		print("LOADING...") #just for fun since it takes a while to scrap the images
csvFile.close()