import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}&jobcatExpansionType=1&order=12&asc=0&page=1&mode=s&jobsource=2018indexpoc'

headers_agent = {
       'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

# ask user to input a keyword
keyword = input('give me a key word:')

# create a session
sess = requests.session()

# use GET to request landing page within the session
req = sess.get(url=url.format(keyword), headers = headers_agent)

# BeautifulSoup
soup = BeautifulSoup(req.text, 'html.parser')
# find all 'div' with class name 'b-block_left'
search_results = soup.findAll('div', class_ = 'b-block__left')

#l = soup.select('article', class_ = "b-block--top-bord job-list-item b-clearfix js-job-item ")
#company = l.findAll('ul', class_ = 'b-list-inline b-clearfix')

#e04 = search_results[3].text
#print(e04)

# go through each element in search_results and use BeautifulSoup select() method to locate all a tag
for i in search_results:
       if len(i.select('a')) == 0:
              pass
       
       #company = i.select('a')[1].text
       #job = i.select('a')[0].text
       else:
              
              job = i.select('a')[0].text
              company = i.select('a')[1].text

              link = i.a['href'] 

              link_job = link[21:26]
              


              #print('https:'+link)
              #print(link_job)
              #print(job)
              #print(company)

ajax_link = 'https://www.104.com.tw/job/ajax/content/703tv'
ajax_headers = {
       'Referer':'https://www.104.com.tw/job/703tv',
       'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
       

}

job_req = requests.get(url=ajax_link, headers = ajax_headers)
data = json.loads(job_req.text)['data']
data_condition = data['condition']

data_specialty = data_condition['specialty']
print(data)
print('--------------------')

specialty_list = []
for j in data_specialty:
       specialty_list.append(j['description'])
print(specialty_list)
print('-------------')

skill = data_condition['skill']
skill_list = []
for i in skill:
       skill_list.append(i['description'])
print (skill_list)
print('--------------')

print(data_condition['other'])
other_list = []
other_list.append(data_condition['other'])
print(other_list)


#df = pd.DataFrame('工具', '技能', '其他')
