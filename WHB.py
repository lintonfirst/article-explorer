# 爬取文汇报
import requests
from bs4 import BeautifulSoup
import threading

def getArticles(year:str,month:str,date:str):
    url="https://dzb.whb.cn/{}/1/index.html".format(year+"-"+month+"-"+date)
    html=requests.get(url)
    html.encoding='utf-8'
    soup=BeautifulSoup(html.text,'html.parser')
    #获取版面
    pageLists=[]
    spaceBox=soup.find('div',id='spaceBox')
    pages=spaceBox.find_all('div',class_='item')
    for page in pages:
        a=page.find('a',class_='TitleInfo')
        pageName=a.get('title')
        pageUrl=a.get('data-href')
        url="https://dzb.whb.cn"+pageUrl
        pageLists.append({'title':pageName,'url':url})
    
    articleLists=[]
    for page in pageLists:
        html=requests.get(page['url'])
        html.encoding='utf-8'
        soup=BeautifulSoup(html.text,'html.parser')
        lists=soup.find('div',class_='title_box')
        for article in lists.find_all('a'):
            url="https://dzb.whb.cn"+article.get('href')
            articleLists.append({"title":article.get_text(),"url":url,"date":year+"-"+month+"-"+date,"page":page['title'],"source":"文汇报"})
    return articleLists

def getAricleDetail(data):
    url=data['url']
    html=requests.get(url)
    html.encoding='utf-8'
    soup=BeautifulSoup(html.text,'html.parser')
    newsContent=soup.find('div',class_='news_content')
    img=newsContent.find('div',class_='img')
    if img:
        img.decompose()
    title_part=newsContent.find('div',class_='title_part')
    if title_part:
        title_part.decompose()
    content=newsContent.get_text()
    content=content.strip()
    paragraphs=content.split('\xa0\xa0\xa0\xa0\xa0\xa0')
    textLength=0
    count=0
    for p in paragraphs:
        p=p.strip()
        if textLength==0 and len(p)>0 and len(p)<20:
            data['author']=p.replace('■','')
        textLength+=len(p)
        if p.find('（作者为')!=-1:
            unit=p[4:-1]
            if unit.find('大学')!=-1 or unit.find('学院')!=-1 or unit.find("党校")!=-1:
                data['unit']=unit
                count+=1
        elif p.find('(作者单位：')!=-1:
            unit=p[6:-1]
            if unit.find('大学')!=-1 or unit.find('学院')!=-1 or unit.find("党校")!=-1:
                data['unit']=unit
                count+=1
    data['textLength']=textLength
    if count==1:
        return data,1
    if count>1:
        return data,count
    return None,0
    

def getWHB(year:str,month:str,date:str):
    lists=getArticles(year,month,date)
    results=[]
    potentials=[]
    threads=[]
    def task(article):
        try:
            res,count=getAricleDetail(article)
            if count==1:
                results.append(res)
            if count>1:
                potentials.append(res)
        except:
            pass
    for article in lists:
        thread=threading.Thread(target=task,args=(article,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results,potentials