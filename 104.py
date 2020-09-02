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

# initialize dataframe df
columns_title = ['職位','公司', '工具', '技能', '其他']
df = pd.DataFrame(columns=columns_title)

# go through each element in search_results and use BeautifulSoup select() method to locate all a tag
for i in search_results:
       if len(i.select('a')) == 0:
              pass
       
       #company = i.select('a')[1].text
       #job = i.select('a')[0].text
       else:
              
              job = i.select('a')[0].text
              company = i.select('a')[1].text.strip()

              link = i.a['href'] 

              link_job = link[21:26]
              ajax_link = 'https://www.104.com.tw/job/ajax/content/{}'.format(link_job)
              ajax_headers = {
                     'Referer':'https://www.104.com.tw/job/{}'.format(link_job),
                     #'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
              }
              job_req = requests.get(url=ajax_link, headers = ajax_headers)
              data = json.loads(job_req.text)['data']
              data_condition = data['condition']
              data_specialty = data_condition['specialty']

              specialty_list = []
              for j in data_specialty:
                     specialty_list.append(j['description'])

              skill = data_condition['skill']
              skill_list = []
              for i in skill:
                     skill_list.append(i['description'])

              other_list = []
              other_list.append(data_condition['other'])

              row_data = [job, company, specialty_list, skill_list, other_list]

              df = df.append({'職位':row_data[0],'公司':row_data[1], '工具':row_data[2], '技能':row_data[3], '其他':row_data[4]}, ignore_index= True)



              #print('https:'+link)
              #print(ajax_link)
              #print(row_data)


df.to_csv('./104.csv', encoding='utf-8', index=False)

print('----------------------------')
print(df)