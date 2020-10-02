"""
python program that uses requests to get HTML/JSON data from 
"""

import requests# getting data from url
from bs4 import BeautifulSoup#parsing data from atcoder,codeforces, no API :\
import pprint#for easy debugging
import urllib.request
from datetime import datetime
from flask import Flask,render_template
from collections import defaultdict

#import pyperclip
class Contest:#self explanatory
    def __init__(self,name,link,time):
        self.name=name
        self.link=link
        self.time=time

class ContestData:
    contest_list=defaultdict(list)
    def get_relative_start_time(self,iso_date):#gettting time in hours for codechef and atcoder
        #print(iso_date)
        converted_date=datetime.fromisoformat(iso_date) 
        #print(converted_date)
        difference=(converted_date-datetime.utcnow().replace(tzinfo=converted_date.tzinfo) )
        return str(int(difference.total_seconds()//3600))+' hours'

    def check_output(self):#checking the list of contests for correct output(at the end of the program)
        for i in self.contest_list.values():
            for j in i:
                print(j.name)
                print(j.link)
                print(j.time)
    def get_code_chef(self):
        #print('codechef')
        codechef_response=requests.get('https://www.codechef.com/contests')
        soup=BeautifulSoup(codechef_response.text,'lxml')
        future_contests_table=soup.find('h3',text='Future Contests').findNext().findAll('a')
        for i in future_contests_table[4:]:
            contest_name='CodeChef '+i.text
            link='https://codechef.com'+i.get('href')
            start_time=i.findNext().get('data-starttime')#.split("T")
            #print(start_time)
            start_time=self.get_relative_start_time(start_time)
            #start_date,start_time=start_time[0],start_time[1].split('+')[0]
            self.contest_list['codechef'].append(Contest(contest_name,link,start_time))

    def get_code_forces(self):
        cf_response=requests.get("https://codeforces.com/api/contest.list")
        cf_dict=cf_response.json()
        cf_status=cf_dict['status']
        cf_res=cf_dict['result'][:10]   
        if cf_status !='OK':
            print("Couldn't get codeforces data, please try again later?")
        else:
            for contest in cf_res:
                if contest['phase']=="FINISHED":
                    break
                else:
                    contest_name=contest['name']
                    link="https://www.codeforces.com/contests"
                    relativeTimeSeconds=contest["relativeTimeSeconds"]
                    self.contest_list['codeforces'].append(Contest(contest_name,link,str(-relativeTimeSeconds//3600)+' hours'))

    def get_at_coder(self):
        at_coder_response=requests.get("https://atcoder.jp/contests/")
        soup=BeautifulSoup(at_coder_response.text,'lxml')
        future_contests_table=soup.find('h3',text='Upcoming Contests').findNext().findAll('a')
        #pprint.pprint(future_contests_table)
        print('atcoder')
        for time,details in zip(future_contests_table[::2],future_contests_table[1::2]): 
            #print(time.text)
                contest_name=details.text
                link="https://atcoder.jp"+details.get('href')
                start_time=time.text.replace(' ','T')
                #print(start_time[:-2]+':'+start_time[-2:])
                start_time=self.get_relative_start_time(start_time[:-2]+':'+start_time[-2:])
                
                self.contest_list['atcoder'].append(Contest(contest_name,link,start_time))

    def get_hacker_rank(self):
        user_agent = ' Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
        url = "https://www.hackerrank.com/contests"
        headers={'User-Agent':user_agent} 
        request=urllib.request.Request(url,None,headers) 
        response = urllib.request.urlopen(request)
        data = response.read() 
        soup=BeautifulSoup(data,'lxml')
        ULtag=soup.find('ul',{'class':'contests-active'})
        names=ULtag.findChildren('span',{'itemprop':'name'})
        start_times=ULtag.findChildren('meta',{'itemprop':"startDate"})
        end_times=ULtag.findChildren('meta',{'itemprop':"endDate"})
        names=[i.text for i in names]
        start_times=[i['content'] for i in start_times]
        #end_times=[i['content'] for i in end_times]
        link='https://www.hackerrank.com/contests'
        for name,start_time in zip(names,start_times):
            start_time=self.get_relative_start_time(start_time[:-5])
            self.contest_list['hackerrank'].append(Contest(name,link,start_time))

    def get_hacker_earth(self):
        user_agent = ' Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
        url = "https://www.hackerearth.com/challenges/"
        headers={'User-Agent':user_agent} 
        request=urllib.request.Request(url,None,headers) 
        response = urllib.request.urlopen(request)
        data = response.read() 
        soup=BeautifulSoup(data,'lxml')
        ULtag=soup.find('ul',{'class':'contests-active'})
        names=ULtag.findChildren('span',{'itemprop':'name'})
        start_times=ULtag.findChildren('meta',{'itemprop':"startDate"})
        end_times=ULtag.findChildren('meta',{'itemprop':"endDate"})
        names=[i.text for i in names]
        start_times=[i['content'] for i in start_times]
        #end_times=[i['content'] for i in end_times]
        link='https://www.hackerearth.com/challenges/'
        for name,start_time in zip(names,start_times):
            start_time=self.get_relative_start_time(start_time[:-5])
            self.contest_list['hackerearth'].append(Contest(name,link,start_time))
                
DoIt=ContestData()
DoIt.get_code_forces()
DoIt.get_code_chef()
DoIt.get_at_coder()
DoIt.get_hacker_rank()
DoIt.get_hacker_earth()
#DoIt.get_leetcode()

DoIt.check_output()
total_list=list()
for i in DoIt.contest_list.values():
    total_list.extend(i)
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',contest_list=total_list)

@app.route('/CF')
def CF():
    return render_template('index.html',contest_list=DoIt.contest_list['codeforces'])


@app.route('/CC')
def CC():
    return render_template('index.html',contest_list=DoIt.contest_list['codechef'])


@app.route('/AC')
def AC():
    return render_template('index.html',contest_list=DoIt.contest_list['atcoder'])

@app.route('/HR')
def HR():
    return render_template('index.html',contest_list=DoIt.contest_list['hackerrank'])
if __name__ == "__main__":

@app.route('/HE')
def HR():
    return render_template('index.html',contest_list=DoIt.contest_list['hackerearth'])
if __name__ == "__main__":


    
    app.run(debug=True)
