import re
from bs4 import BeautifulSoup
import requests
# Reading from URL and using BeautifulSoup to find patterns
r = requests.get('https://maktabkhooneh.org/plus/')
soup = BeautifulSoup(r.text,'html.parser')

#s = soup.find_all('div', attrs={'class':'course-name'})
#s = soup.find_all('a',attrs={'href':re.compile(r"^/course/\d{3}/.+")})
#s = soup.find_all('img',attrs={'class':'course-picture'})['title']
s = soup.find_all(id='name')
o = soup.find_all(id='org')
#--------------------------------------------------------------
#for a in soup.find_all('a',attrs={'href':re.compile(r"^/course/\d{3}/.+")}):
#    if a.img and a.div.span['id'] == 'org':
#        print(a.img['title'])
#Match the criteria of Maktabkhooneh courses
title = []
organization = []
for i in s:
    title.append(re.sub('[\s+\\u200c]',' ',i.text).strip())
for j in o:
    organization.append(re.sub('[\s+\\u200c]',' ',j.text).strip())
for i in range(len(s)):
    if organization[i] == 'مکتب خونه':
        print(title[i])

# v = 'برنامه نویسی'
# f = list(filter(lambda x: v in x, title))
# print(f)



