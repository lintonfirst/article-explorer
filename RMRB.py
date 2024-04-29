# 爬取人民日报
import requests
import re
from bs4 import BeautifulSoup
import csv
import json

def getArticles(year:str,month:str,date:str):
    url = "http://paper.people.com.cn/rmrb/html/"+year+"-"+month+"/"+date+"/nbs.D110000renmrb_01.htm"
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'html.parser')
    #获取版面
    pageLists=[] #01版，#02版 ...
    for page in soup.find_all('div',class_='swiper-slide'):
        pageTitle=page.find('a').get_text()
        pageUrl=page.find('a').get('href')
        url = "http://paper.people.com.cn/rmrb/html/"+year+"-"+month+"/"+date+"/"+pageUrl
        pageLists.append({'title':pageTitle,'url':url})
    
    articleLists=[]
    for page in pageLists:
        html = requests.get(page['url'])
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'html.parser')
        #获取文章
        lists=soup.find('ul',class_='news-list')
        for article in lists.find_all('a'):
            url="http://paper.people.com.cn/rmrb/html/"+year+"-"+month+"/"+date+"/"+article.get('href')
            articleLists.append({"title":article.get_text(),"url":url,"date":year+"-"+month+"-"+date,"page":page['title'],"source":"人民日报"})
            
    return articleLists
    
def getAricleDetail(data):
    url = data['url']
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup=BeautifulSoup(html.text,'html.parser')
    article=soup.find('div',class_='article')
    author=article.find('p',class_='sec')
    #删除内部的span标签
    author.span.decompose()
    if author:
        author=author.get_text()
        data['author']=author
    ozoom=article.find('div',id='ozoom')
    paragraphs=ozoom.find_all('p')
    textLength=0
    
    count=0
    
    for p in paragraphs:
        textLength+=len(p.get_text())
        text=p.get_text().strip()
        if text.find('（作者为')!=-1:
            unit=text[4:len(text)-1]
            if unit.find('大学')!=-1 or unit.find('学院')!=-1 or unit.find("党校")!=-1:
                data['unit']=unit
                count+=1
        if text.find('（作者分别为')!=-1:
            unit=text[6:len(text)-1]
            if unit.find('大学')!=-1 or unit.find('学院')!=-1 or unit.find("党校")!=-1:
                data['unit']=unit
                count+=1
    data['textLength']=textLength
    if count==1:
        return data,1
    if count>1:
        return data,count
    return None,0
    
def getRMRB(year:str,month:str,date:str):
    lists=getArticles(year,month,date)
    results=[]
    potentials=[]
    for article in lists:
        res,count=getAricleDetail(article)
        if count==1:
            results.append(res)
        if count>1:
            potentials.append(res)
    return results,potentials



