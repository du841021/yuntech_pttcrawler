
# coding: utf-8

# In[23]:


import os
import json
import requests
from uuid import uuid4
from bs4 import BeautifulSoup

class Pttcrawler:
    def __init__(self,board,page,write=False):
        self.ptt_url='https://www.ptt.cc'
        self.board=board
        self.page=page
        self.session=requests.Session()
        self.session.cookies.update({
            'over18':'1'
        })
        #self.write=write
    
    def run(self):
        url=self.ptt_url+'/bbs'+self.board
        post_link_list=self.fetchPostLinklist(url)
        post_list=[self.fetchPost(post_link) for post_link in post_link_list]
#        if self.write:
#            result_dir=os.path.join('ptt_crawler/'+str(uuid4()))
#            os.makedirs(result_dir,exit_ok=True)
#            for post in post_list:
#                with open(os.path.join(result_dir,post['id']),'w')as f:
#                    f.write(josn.dumps(post,indent=4))
        print(post_list)
        return post_list
    
    def fetchPostLinklist(self,url):
        if not url.startswith('http'):
            url=self.ptt_url+url
        resp=self.session.get(url)
        
        soup=BeautifulSoup(resp.text.encode("utf-8"),"lxml")
        post_list=soup.find('div',{'class':'r-list-container action-bar-margin bbs-screen'})
        link_list=[tag.get('href')for tag in post_list.find_all('a')]
        
        return link_list
    
    def fetchPost(self,url):
        resp=requests.get(
        'https://www.ptt.cc'+url,
        cookies={'over18':'1'})
        soup=BeautifulSoup(resp.text.encode("utf-8"),"lxml")
        if soup.find('title'):
            title=soup.find('title').text
        else:
            title=None
        if soup.find('span',{'class':'article-meta-value'}):
            author=soup.find('span',{'class':'article-meta-value'}).text
        else:
            author=None
        return{'title':title,'author':author}
    


# In[25]:


ohyeah=Pttcrawler('/Gossiping/',1)
a = ohyeah.run()

