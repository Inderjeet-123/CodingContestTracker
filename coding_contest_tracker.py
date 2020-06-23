import requests
from bs4 import BeautifulSoup
class Contest:
    def __init__(self,name,link,time):
        self.name=name
        self.link=link
        self.time=time

codechef_response=requests.get('https://www.codechef.com/contests')
soup=BeautifulSoup(codechef_response.text,'lxml')
future_contests_table=soup.find('h3',text='Future Contests').findNext().findAll('a')
contest_list=[]
for i in future_contests_table[4:]:
    contest_name='CodeChef '+i.text
    link='codechef.com'+i.get('href')
    start_time=i.findNext().get('data-starttime').split("T")
    start_date,start_time=start_time[0],start_time[1].split('+')[0]
    contest_list.append(Contest(contest_name,link,start_time))
cf_response=requests.get("https://codeforces.com/api/contest.list")
cf_json=cf_response.json()
cf_status=cf_json['status']
cf_res=cf_json['result'][:10]   
if cf_status !='OK':
    print("Couldn't get codeforces data, please try again later?")
else:
    for contest in cf_res:
        if contest['phase']=="FINISHED":
            break
        else:
            contest_name=contest['name']
            link="https://www.codeforces.com/contest"
            relativeTimeSeconds=contest["relativeTimeSeconds"]
            contest_list.append(Contest(contest_name,link,str(-relativeTimeSeconds//3600)+' hours'))

